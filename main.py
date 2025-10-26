import os
import eel
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

    port: int = int(os.getenv("APP_PORT", 7666))

    eel.init(os.path.join(os.path.dirname(__file__), "ui", "frontend", "dist"))
    eel.start("index.html", mode="browser", port=port)
