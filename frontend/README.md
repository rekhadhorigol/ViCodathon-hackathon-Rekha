# Intmate — Frontend

React + Vite single-page app for Intmate, the AI interview agent.

## Setup

```bash
npm install
npm run dev
```

## Environment variables

- `VITE_API_BASE` — base URL of the backend API (e.g. `http://localhost:8000` locally,
  or your deployed backend URL in production).
- `VITE_USE_MOCK_API` — set to `true` to run the UI against `src/services/mockApi.js`
  without a backend, useful for demos or frontend-only development.

## Pages

- `/` — landing page
- `/setup` — pick a candidate and start a session
- `/interview` — the live, multi-turn interview
- `/results` — final AI-generated assessment
