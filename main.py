import os
import eel
from dotenv import load_dotenv
import bridge
from noita_libs.noita_backup_helper import NoitaBackupHelper
from setting_libs.setting_helper import SettingHelper


def initialize_settings():
    """Initialize settings with default values if they do not exist"""
    default_settings = {
        "noita_saves_dir_path": "/mnt/c/Users/user/AppData/LocalLow/Nolla_Games_Noita",
        "backup_dir_path": "./data/backups",
        "backup_filename": "backups.json",
    }

    for key, value in default_settings.items():
        if SettingHelper.get_setting(key) is None:
            SettingHelper.save_setting(key, value)


def start_app():
    """Start the Eel application"""
    port: int = int(os.getenv("APP_PORT", 7666))

    eel.init(os.path.join(os.path.dirname(__file__), "ui", "frontend", "dist"))

    eel.start("index.html", mode="browser", port=port)


def expose_bridge_functions():
    """Expose bridge functions to the frontend through Eel"""

    def get_backups():
        return bridge.get_backups(noita_backup_helper)

    eel.expose(get_backups)


if __name__ == "__main__":
    load_dotenv()
    initialize_settings()

    noita_saves_dir_path: str = SettingHelper.get_setting("noita_saves_dir_path")
    backup_dir_path: str = SettingHelper.get_setting("backup_dir_path")
    backup_filename: str = SettingHelper.get_setting("backup_filename")

    print("Noita Saves Dir Path:", noita_saves_dir_path)
    print("Backup Dir Path:", backup_dir_path)
    print("Backup Filename:", backup_filename)

    noita_backup_helper: NoitaBackupHelper = NoitaBackupHelper(
        noita_saves_dir_path=noita_saves_dir_path,
        backup_dir_path=backup_dir_path,
        backup_filename=backup_filename,
    )

    expose_bridge_functions()
    start_app()
