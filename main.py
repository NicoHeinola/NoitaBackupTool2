import os
import sys
from pathlib import Path
import eel
from dotenv import load_dotenv
import bridge
from noita_libs.noita_backup_helper import NoitaBackupHelper
from setting_libs.setting_helper import SettingHelper
import logging

logger = logging.getLogger(__name__)


def initialize_settings():
    """Initialize settings with default values if they do not exist"""

    default_settings = {
        "noita_saves_dir_path": "/mnt/c/Users/user/AppData/LocalLow/Nolla_Games_Noita",
        "backup_dir_path": "./data/backups",
        "backup_filename": "backups.json",
    }

    for key, value in default_settings.items():
        setting: str = SettingHelper.get_setting(key)
        if setting is None or setting == "":
            result = SettingHelper.save_setting(key, value)
            if result is None or isinstance(result, dict) and not result.get("success", True):
                logger.warning(f"Failed to initialize setting {key}")
    logger.info("Settings initialized successfully.")


def start_app():
    """Start the Eel application"""
    port: int = int(os.getenv("APP_PORT", 7666))

    eel.init(os.path.join(os.path.dirname(__file__), "ui", "frontend", "dist"))

    eel.start(
        "",
        mode="browser",
        port=port,
    )


def apply_settings_changes():
    """Apply settings changes to the NoitaBackupHelper instance"""
    try:
        noita_saves_dir_path_response = bridge.get_setting("noita_saves_dir_path")
        backup_dir_path_response = bridge.get_setting("backup_dir_path")
        backup_filename_response = bridge.get_setting("backup_filename")

        if noita_saves_dir_path_response.get("success"):
            noita_backup_helper.noita_saves_dir_path = noita_saves_dir_path_response.get("data")

        if backup_dir_path_response.get("success"):
            noita_backup_helper.backups_dir_path = backup_dir_path_response.get("data")

        if backup_filename_response.get("success"):
            noita_backup_helper.backups_filename = backup_filename_response.get("data")
    except Exception as e:
        logger.error(f"Error applying settings changes: {e}")


def expose_bridge_functions():
    """Expose bridge functions to the frontend through Eel"""

    # Backups
    def get_backups():
        return bridge.get_backups(noita_backup_helper)

    def save_backup(backup_data):
        return bridge.save_backup(noita_backup_helper, backup_data)

    def delete_backup(backup_id):
        return bridge.delete_backup(noita_backup_helper, backup_id)

    def load_backup(backup_id):
        return bridge.load_backup(noita_backup_helper, backup_id)

    def duplicate_backup(backup_id, new_backup_data=None):
        return bridge.duplicate_backup(noita_backup_helper, backup_id, new_backup_data)

    def replace_backup(backup_id):
        return bridge.replace_backup(noita_backup_helper, backup_id)

    eel.expose(get_backups)
    eel.expose(save_backup)
    eel.expose(delete_backup)
    eel.expose(load_backup)
    eel.expose(duplicate_backup)
    eel.expose(replace_backup)

    # Settings
    def get_setting(key, default_value=""):
        return bridge.get_setting(key, default_value)

    def save_setting(key, value):
        result = bridge.save_setting(key, value)

        # Only apply settings changes if the save was successful
        if result.get("success", False):
            apply_settings_changes()

        return result

    def save_settings(settings_data):
        results = bridge.save_settings(settings_data)

        # Only apply settings changes if the save was successful
        if results.get("success", False):
            apply_settings_changes()

        return results

    def get_all_settings():
        return bridge.get_all_settings()

    eel.expose(get_setting)
    eel.expose(save_setting)
    eel.expose(save_settings)
    eel.expose(get_all_settings)


def load_env():
    # Load .env from project root during development or from the
    # PyInstaller temporary folder when frozen (sys._MEIPASS).
    # This ensures bundled apps can include a .env via --add-data.
    if getattr(sys, "frozen", False):
        # avoid direct attribute access (Pylance warns for sys._MEIPASS)
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            base_path = Path(meipass)
            env_path = base_path / ".env"
            if env_path.exists():
                load_dotenv(dotenv_path=str(env_path))
    else:
        # normal development
        load_dotenv()


if __name__ == "__main__":
    load_env()
    initialize_settings()

    noita_saves_dir_path: str = SettingHelper.get_setting("noita_saves_dir_path")
    backup_dir_path: str = SettingHelper.get_setting("backup_dir_path")
    backup_filename: str = SettingHelper.get_setting("backup_filename")

    noita_backup_helper: NoitaBackupHelper = NoitaBackupHelper(
        noita_saves_dir_path=noita_saves_dir_path,
        backup_dir_path=backup_dir_path,
        backup_filename=backup_filename,
    )

    expose_bridge_functions()
    start_app()
