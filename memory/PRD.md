# PRD — Planner PWA (Organizzatore Settimanale)

## Problem Statement
"Sistema tutti i fix e rendilo installabile PWA ed utilizzabile memorizzando il login."

Unificare le tre versioni (`index.html`, `index-v2.html`, `index-v2.1.html`) in un'unica app statica ottimizzata, sistemare tutti i bug, rendere l'app installabile come PWA e ricordare il login Google tra le sessioni.

## Architecture
- **Static single-page app**: `index.html` + `manifest.json` + `sw.js`
- **Storage**: `localStorage` per eventi, token Google, preferenze UI
- **Auth**: Google OAuth2 (GIS + GAPI), client-side only, token con expiry
- **Calendar sync**: Google Calendar API (opzionale, app funziona anche offline)
- **Hosting**: statico (serve `/app` su porta 3000 tramite `serve`)

## User Persona
Utente italiano che vuole un'agenda settimanale leggera, installabile su mobile, con opzionale sync Google Calendar, utilizzabile anche offline.

## Core Requirements (static)
1. Agenda giornaliera con slot da 30 min (7:00–21:00)
2. Eventi con titolo, durata, categoria, note
3. Swipe/arrow-keys per cambiare giorno
4. Scroll giorni (±30 / +730)
5. Festività italiane auto-rilevate
6. Dark mode
7. Persistenza login Google + eventi
8. Installabile come PWA (Android/iOS)
9. Funziona offline (shell cache + eventi locali)

## Implementation Status (v3.1.0 — Apr 2026)
- [x] Unificato in singolo `index.html` (v2.1 come base)
- [x] Rimossi `index-v2.html` e `index-v2.1.html`
- [x] Token Google persistente con `expires_at` + refresh silenzioso
- [x] Auto-restore sessione all'avvio (user info da cache + token valido)
- [x] Su 401 non elimina dati locali (solo mostra "accedi per rinnovare")
- [x] PWA manifest con `id`, `start_url: ./index.html`, icons any+maskable
- [x] SW v3: network-first per navigation, cache-first per shell, bypass Google APIs
- [x] Install banner con fallback iOS ("Aggiungi a Home")
- [x] Dark mode con toggle icona dinamica + theme-color meta update
- [x] Safe-area iOS (notch) tramite `env(safe-area-inset-*)`
- [x] Fix swipe vs click (suppressNextClick per evitare apertura modal dopo swipe)
- [x] Fix XSS su titoli evento (escapeHtml)
- [x] data-testid su tutti gli elementi interattivi
- [x] Online/offline detection con toast + auto-sync su ripristino
- [x] Auto-sync ogni 5 minuti solo se visibile e signed-in
- [x] Sync al ritorno in foreground (visibilitychange)
- [x] Keyboard shortcuts (Escape, ←→, Ctrl/Cmd+Enter save)
- [x] Welcome screen al primo avvio (spiega sync Google Calendar cross-device)
- [x] Favicon reale (16/32 PNG + ICO + 180 apple-touch-icon + 192/512 maskable)
- [x] FAB (Floating Action Button) per creazione rapida evento al prossimo slot
- [x] Touch target aumentati (min-height 48px hour-slot)
- [x] Day-chip active con scale + shadow
- [x] Overscroll pull-to-refresh disabilitato
- [x] Deployment-ready: backend FastAPI minimale + frontend con build script

## Structure
```
/app
├── backend/
│   ├── server.py         # Minimal FastAPI (health endpoints only, /api/ and /api/health)
│   ├── requirements.txt  # fastapi, uvicorn, pydantic, python-dotenv
│   └── .env              # MONGO_URL, DB_NAME, CORS_ORIGINS
├── frontend/
│   ├── public/           # Source static files
│   │   ├── index.html    # Main app (HTML+CSS+JS)
│   │   ├── manifest.json # PWA manifest
│   │   └── sw.js         # Service worker v3
│   ├── build/            # Build output (served)
│   ├── package.json      # scripts: build (copy public→build) + start (serve build)
│   └── .env              # REACT_APP_BACKEND_URL
└── memory/PRD.md
```

## Deployment
- Frontend: `yarn install && yarn build` → `yarn start` serves `build/` on port 3000
- Backend: `uvicorn server:app --host 0.0.0.0 --port 8001` exposes `/api/` and `/api/health`
- Health check: GET `/api/health` returns `{status: ok}`
- No MongoDB actually used (env vars present to satisfy platform requirements)

## Backlog / Future Enhancements
- **P1** Esportazione eventi (CSV/ICS)
- **P1** Notifiche push prima dell'evento
- **P2** Vista settimanale/mensile
- **P2** Ricerca eventi
- **P2** Ripetizione locale (già presente per Google)
- **P2** Backup/restore localStorage (JSON import/export)
- **P3** Sincronizzazione multi-dispositivo (richiederebbe backend)

## Tech Notes
- Google Client ID hardcoded (progetto esistente)
- Token access_token durata ~1h → buffer 30s prima di considerarlo scaduto
- SW bypassa totalmente le chiamate a `googleapis.com`, `accounts.google.com`, `gstatic.com`
- Cache versione: `planner-v3.0.0` (incrementare su major changes)
