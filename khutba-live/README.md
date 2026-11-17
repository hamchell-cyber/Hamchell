# Traduction en direct de la khutba (darija → français) sur écran TV

```
 Micro de l'imam ─► Table de mixage ─► Carte son USB ─► Mini-PC ─HDMI─► TV
                                                          │
                     ┌────────────────────────────────────┘
                     ▼
   1. Reconnaissance vocale  Azure Speech « ar-MA » + lexique islamique (phrase list)
   2. Traduction             Claude (contexte des phrases précédentes + lexique imposé)
   3. Affichage              Page web plein écran (Chromium kiosque), mise à jour WebSocket
```

Latence visée : 2 à 4 s après la fin de chaque phrase de l'imam.

## Matériel (≈ 250–400 €)

| Élément | Conseil |
|---|---|
| Mini-PC | Intel N100 / Raspberry Pi 5 (8 Go) avec sortie HDMI |
| Audio | **Prendre le son sur la table de mixage** (sortie AUX/REC) via une carte son USB (ex. Behringer UCA202). Un micro posé dans la salle capte l'écho → mauvaise reconnaissance. |
| Réseau | Ethernet de préférence (4G en secours) |
| Écran | TV 50"+ ; texte réglable avec `+` / `-` |

## Installation

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

```bash
cp config.example.env .env   # puis remplir les clés
```

```bash
set -a; source .env; set +a; .venv/bin/uvicorn app.server:app --host 0.0.0.0 --port 8000
```

```bash
chromium --kiosk --noerrdialogs --disable-infobars http://localhost:8000
```

Démo sans micro ni clé Azure (rejoue `exemples/khutba_demo.txt`) : ajouter `DEMO_FICHIER=exemples/khutba_demo.txt` dans `.env`.

Raccourcis sur l'écran : `A` afficher/masquer l'arabe · `+`/`-` taille · `C` effacer.

## Fichiers

- `app/glossary.py` — **lexique islamique** et darija : à enrichir avec le vocabulaire de votre imam.
- `app/stt.py` — reconnaissance vocale continue (Azure) ou mode démo.
- `app/translator.py` — consignes de traduction (versets, hadiths, eulogies, ﷺ…).
- `app/server.py` — orchestration + WebSocket.
- `static/display.html` — écran TV (traduction en grand, arabe en petit, texte en cours en bas).

## Points d'attention

- **Darija** : aucun moteur n'est parfait. `ar-MA` d'Azure gère le mélange fusha/darija correctement ;
  Claude corrige une partie des erreurs grâce au contexte. Tester sur 2–3 khoutbas enregistrées
  avant la mise en service, et enrichir le lexique avec les mots mal reconnus.
- **Versets du Coran** : le traducteur ne donne une référence que s'il en est sûr. Pour plus de
  rigueur, l'imam peut fournir à l'avance les versets/hadiths de la khutba (à ajouter au prompt).
- **Validation religieuse** : faire relire le lexique et quelques traductions par l'imam ou le conseil
  de la mosquée ; afficher une mention « traduction automatique » si souhaité.
- **Coût indicatif** : quelques dizaines de centimes à ~1 € par khutba de 30 min (Azure STT + Claude).
- **Autres langues** : changer `LANGUE_CIBLE` (anglais, espagnol…). Pour plusieurs langues
  simultanées, lancer une boucle de traduction par langue.
