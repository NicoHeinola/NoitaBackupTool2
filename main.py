import os
import eel
from dotenv import load_dotenv
import bridge

if __name__ == "__main__":
    load_dotenv()

    port: int = int(os.getenv("APP_PORT", 7666))

    eel.init(os.path.join(os.path.dirname(__file__), "ui", "frontend", "dist"))

    # expose bridge functions to the frontend through Eel
    eel.expose(bridge.get_backups)

    eel.start("index.html", mode="browser", port=port)
