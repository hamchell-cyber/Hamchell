"""Traduction darija/arabe → français (ou autre langue) avec Claude, en streaming."""
from __future__ import annotations

import os
from collections import deque
from typing import AsyncIterator

import anthropic

from .glossary import glossaire_texte

MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5-5")
LANGUE_CIBLE = os.getenv("LANGUE_CIBLE", "français")

SYSTEM = f"""Tu es l'interprète simultané d'une mosquée au Maroc. Tu reçois, phrase par phrase, la
transcription automatique (donc imparfaite) du sermon (khutba) d'un imam qui mélange arabe classique
(fusha) et darija marocaine. Ta traduction est projetée en direct sur un écran pour les fidèles.

Règles :
1. Traduis UNIQUEMENT le nouveau segment en {LANGUE_CIBLE}, de façon fidèle, respectueuse et sobre.
   N'ajoute ni commentaire, ni explication, ni guillemets autour de ta réponse.
2. La transcription contient des erreurs de reconnaissance : sers-toi du contexte et du lexique
   pour corriger les mots mal reconnus. Si un passage est incompréhensible, omets-le plutôt que d'inventer.
3. Versets du Coran : si tu reconnais un verset, donne son sens en {LANGUE_CIBLE} entre « », suivi de
   la référence entre crochets si tu en es certain, ex. [Al-Baqara, 2:183]. Ne cite jamais une référence douteuse.
4. Hadiths : traduis le sens ; garde « le Prophète ﷺ ».
5. Respecte strictement le lexique ci-dessous (Allah reste « Allah », formules d'eulogie conservées).
6. Phrases courtes, lisibles sur un écran : 1 à 3 lignes maximum par segment.
7. Si le segment n'est qu'une hésitation ou un bruit, réponds par une chaîne vide.

{glossaire_texte()}
"""


class Traducteur:
    def __init__(self, contexte: int = 6):
        self.client = anthropic.AsyncAnthropic()
        self.historique: deque[tuple[str, str]] = deque(maxlen=contexte)

    async def traduire(self, segment: str) -> AsyncIterator[str]:
        """Produit la traduction morceau par morceau (pour affichage progressif)."""
        ctx = "\n".join(f"[AR] {a}\n[FR] {f}" for a, f in self.historique) or "(début du sermon)"
        user = (
            f"Contexte précédent :\n{ctx}\n\n"
            f"Nouveau segment à traduire :\n{segment}"
        )
        morceaux: list[str] = []
        async with self.client.beta.messages.stream(
            model=MODEL,
            max_tokens=2000,
            # Latence minimale : effort bas ; le prompt système (lexique) est mis en cache.
            output_config={"effort": "low"},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": user}],
        ) as stream:
            async for texte in stream.text_stream:
                morceaux.append(texte)
                yield texte
            final = await stream.get_final_message()
        if final.stop_reason == "refusal":
            return
        self.historique.append((segment, "".join(morceaux).strip()))
