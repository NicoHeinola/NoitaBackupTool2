"""Bridge for python and frontend code to communicate"""

from noita_libs.noita_backup_helper import NoitaBackupHelper
from noita_libs.noita_backup import NoitaBackup
from setting_libs.setting_helper import SettingHelper
from typing import Any


def get_backups(noita_backup_helper: NoitaBackupHelper) -> list[dict]:
    """Return all backups as serialized dicts."""
    result = noita_backup_helper.get_all_backups()

    return [backup.serialize() for backup in result]


def save_backup(noita_backup_helper: NoitaBackupHelper, backup_data: dict) -> dict:
    """Save a backup record and create a zip of the current save files.

    Expects backup_data to be a dict matching NoitaBackup.serialize() shape.
    Returns the saved backup as a serialized dict (including assigned id).
    """
    backup = NoitaBackup()
    backup.deserialize(backup_data)

    noita_backup_helper.save_backup(backup)

    return backup.serialize()


def delete_backup(noita_backup_helper: NoitaBackupHelper, backup_id: str) -> None:
    """Delete the backup with the given id (removes record; zip file remains or is managed by helper)."""
    noita_backup_helper.delete_backup(backup_id)


def load_backup(noita_backup_helper: NoitaBackupHelper, backup_id: str) -> None:
    """Load the backup with the given id into the current Noita save directory."""
    noita_backup_helper.load_backup(backup_id)


def duplicate_backup(noita_backup_helper: NoitaBackupHelper, backup_id: str, new_backup_data: dict | None = None) -> dict:
    """Create a copy of an existing backup with a new ID.
    
    Args:
        noita_backup_helper: The backup helper instance
        backup_id: The ID of the backup to duplicate
        new_backup_data: Optional dict with new name/description/date for the duplicated backup
        
    Returns:
        The newly created backup as a serialized dict
    """
    new_backup = noita_backup_helper.duplicate_backup(backup_id, new_backup_data)
    return new_backup.serialize()


def replace_backup(noita_backup_helper: NoitaBackupHelper, backup_id: str) -> None:
    """Replace the backup files of the given backup ID with the current Noita save.
    
    Args:
        noita_backup_helper: The backup helper instance
        backup_id: The ID of the backup to replace
    """
    noita_backup_helper.replace_backup(backup_id)


def get_setting(key: str, default: Any = "") -> Any:
    """Retrieve a single setting value."""
    return SettingHelper.get_setting(key, default)


def save_setting(key: str, value: Any) -> None:
    """Save a single setting key/value pair."""
    SettingHelper.save_setting(key, value)


def save_settings(settings_data: dict) -> None:
    """Save all settings from a dict."""
    SettingHelper.save_settings(settings_data)


def get_all_settings() -> dict:
    """Return all settings as a dict."""
    return SettingHelper.load_settings()
