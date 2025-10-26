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

Result: `dist/NoitaBackupTool2/` contains the `.exe` and required files — copy that folder to Windows to test.

Loading `.env` from the bundled folder

Use this small helper so `.env` is found both during development and in the PyInstaller bundle (requires `python-dotenv`):

```python
import sys
from pathlib import Path
from dotenv import load_dotenv

base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
env = base / ".env"
if env.exists():
    load_dotenv(dotenv_path=str(env))
```
