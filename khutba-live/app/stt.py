"""Reconnaissance vocale en continu.

- AzureSTT : Azure AI Speech, locale « ar-MA » (arabe marocain), avec liste de phrases
  islamiques pour améliorer la reconnaissance. Entrée : micro / carte son par défaut du système
  (branchez la sortie de la table de mixage de la mosquée sur une carte son USB).
- FichierSTT : rejoue un fichier texte ligne par ligne (démo / test sans micro ni clé Azure).
"""
from __future__ import annotations

import asyncio
import os
from typing import Awaitable, Callable

from .glossary import phrases_pour_stt

OnPartial = Callable[[str], Awaitable[None]]
OnFinal = Callable[[str], Awaitable[None]]


class AzureSTT:
    def __init__(self, on_partial: OnPartial, on_final: OnFinal):
        self.on_partial, self.on_final = on_partial, on_final

    async def run(self):
        import azure.cognitiveservices.speech as speechsdk

        loop = asyncio.get_running_loop()
        cfg = speechsdk.SpeechConfig(
            subscription=os.environ["AZURE_SPEECH_KEY"], region=os.environ["AZURE_SPEECH_REGION"]
        )
        cfg.speech_recognition_language = os.getenv("STT_LANGUE", "ar-MA")
        # Segmentation : un silence de ~600 ms clôt une phrase (l'imam marque des pauses).
        cfg.set_property(speechsdk.PropertyId.Speech_SegmentationSilenceTimeoutMs, os.getenv("SILENCE_MS", "600"))
        audio = speechsdk.audio.AudioConfig(use_default_microphone=True)
        reco = speechsdk.SpeechRecognizer(speech_config=cfg, audio_config=audio)

        phrases = speechsdk.PhraseListGrammar.from_recognizer(reco)
        for p in phrases_pour_stt():
            phrases.addPhrase(p)

        def partial(evt):
            asyncio.run_coroutine_threadsafe(self.on_partial(evt.result.text), loop)

        def final(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech and evt.result.text.strip():
                asyncio.run_coroutine_threadsafe(self.on_final(evt.result.text), loop)

        reco.recognizing.connect(partial)
        reco.recognized.connect(final)
        reco.canceled.connect(lambda e: print("STT annulé :", e.cancellation_details.error_details))
        reco.start_continuous_recognition_async().get()
        print("🎙️  Reconnaissance ar-MA démarrée")
        try:
            await asyncio.Event().wait()
        finally:
            reco.stop_continuous_recognition_async().get()


class FichierSTT:
    def __init__(self, on_partial: OnPartial, on_final: OnFinal, chemin: str, pause: float = 4.0):
        self.on_partial, self.on_final, self.chemin, self.pause = on_partial, on_final, chemin, pause

    async def run(self):
        await asyncio.sleep(2)
        with open(self.chemin, encoding="utf-8") as f:
            lignes = [l.strip() for l in f if l.strip()]
        for ligne in lignes:
            mots = ligne.split()
            for i in range(1, len(mots) + 1):  # simule les résultats partiels
                await self.on_partial(" ".join(mots[:i]))
                await asyncio.sleep(0.15)
            await self.on_final(ligne)
            await asyncio.sleep(self.pause)
