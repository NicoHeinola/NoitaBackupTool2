# NoitaBackupTool2

A rewamped version of NoitaBackupSaver.

## Installation (Unix terminals)

1. Optional: create & activate venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python deps

```bash
pip install -r requirements.txt
```

3. Build frontend

```bash
cd ui/frontend
npm install
npm run build
cd -
```

4. Create `.env` from `.env.example` (if needed)

```bash
cp .env.example .env
# edit .env as required
```

5. Run app

```bash
python3 main.py
```

## Build (Windows .exe — Unix shell)

Create a folder-based Windows build using PyInstaller (Unix shell only):

1. Install PyInstaller

```bash
pip install pyinstaller
```

2. Run PyInstaller (use `:` as `--add-data` separator on Unix)

```bash
pyinstaller --onedir --windowed --name NoitaBackupTool2 \
  --icon assets/icon.ico \
  --add-data ".env:." \
  --add-data "ui/frontend/dist:ui/frontend/dist" \
  main.py
```
