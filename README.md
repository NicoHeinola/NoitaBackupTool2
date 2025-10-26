# NoitaBackupTool2

A rewamped version of NoitaBackupSaver that I made a few years ago.

# Installation

Minimum, quick steps to get the app running locally:

1. Create and activate a Python virtual environment (optional but recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
```

3. Install and build the frontend

```bash
cd ui/frontend
npm install
npm run build
```

4. Create `.env` file based on `.env.example`

5. Run the application

```bash
python3 main.py
```
