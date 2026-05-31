# Noita Backup Tool Frontend

This frontend is the Vue 3 + Vuetify UI for managing Noita backup files and save state workflows.

## Requirements

- Node.js 22 or newer
- npm

## Quick Start

```bash
cd ui/frontend
npm install
npm run dev
```

If you need a custom port, set `APP_PORT` before starting the app:

```bash
APP_PORT=4173 npm run dev
```

## Available Commands

```bash
npm run dev
npm run preview
npm run build
npm run type-check
npm run check:lint
npm run check:format
npm run check
npm run fix:lint
npm run fix:format
npm run fix
```

## Project Structure

- `src/pages` — route-level pages
- `src/components` — reusable UI and feature components
- `src/components/dialogs` — dialog-driven components and workflows
- `src/components/blocks` — shared UI blocks such as snackbar and tables
- `src/plugins` — plugin registration and app bootstrap
- `src/router` — Vue Router configuration
- `src/stores` — Pinia stores for persisted state
- `src/utils` — shared helpers and utilities

## Frontend Conventions

- Use composables like `useDialog()` and `useSnackbar()` for dialog and snackbar flows.
- Keep dialog presentation inside dedicated components and emit `resolve` / `close` events for callers.
- Centralize backend error feedback with `errorSnackbar()`.
- Prefer explicit TypeScript typings for composables and providers.

## Current Status

The frontend includes backup list management, edit/create dialogs, settings dialogs, and snackbar feedback. Core dialog and notification systems are designed for reusable workflows.
