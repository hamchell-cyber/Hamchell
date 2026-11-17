"""Serveur : reconnaissance vocale → traduction → diffusion WebSocket vers l'écran HDMI.

Lancement :
    uvicorn app.server:app --host 0.0.0.0 --port 8000
Écran : ouvrir http://localhost:8000 en plein écran (mode kiosque).
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from .stt import AzureSTT, FichierSTT
from .translator import Traducteur

STATIC = Path(__file__).resolve().parent.parent / "static"
app = FastAPI()
ecrans: set[WebSocket] = set()
traducteur = Traducteur()
file_segments: asyncio.Queue[str] = asyncio.Queue()
compteur = 0


async def diffuser(msg: dict):
    data = json.dumps(msg, ensure_ascii=False)
    for ws in list(ecrans):
        try:
            await ws.send_text(data)
        except Exception:
            ecrans.discard(ws)


async def on_partial(texte: str):
    await diffuser({"type": "partiel", "ar": texte})


async def on_final(texte: str):
    await file_segments.put(texte)


async def boucle_traduction():
    """Traduit les segments dans l'ordre (un à la fois pour garder le contexte cohérent)."""
    global compteur
    while True:
        seg = await file_segments.get()
        compteur += 1
        sid = compteur
        await diffuser({"type": "debut", "id": sid, "ar": seg})
        try:
            async for morceau in traducteur.traduire(seg):
                await diffuser({"type": "morceau", "id": sid, "txt": morceau})
        except Exception as e:  # ne jamais bloquer l'écran pendant la khutba
            print("Erreur traduction :", e)
        await diffuser({"type": "fin", "id": sid})


@app.on_event("startup")
async def demarrer():
    asyncio.create_task(boucle_traduction())
    demo = os.getenv("DEMO_FICHIER")
    stt = FichierSTT(on_partial, on_final, demo) if demo else AzureSTT(on_partial, on_final)
    asyncio.create_task(stt.run())


@app.get("/")
async def ecran():
    return FileResponse(STATIC / "display.html")


@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    ecrans.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ecrans.discard(websocket)
