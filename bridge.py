"""Bridge for python and frontend code to communicate"""

from noita_libs.noita_backup_helper import NoitaBackupHelper
from noita_libs.noita_backup import NoitaBackup
from setting_libs.setting_helper import SettingHelper
from typing import Any
import logging

logger = logging.getLogger(__name__)


def _success_response(data: Any = None) -> dict:
    """Create a standardized success response."""
    return {"success": True, "data": data, "error": None}


def _error_response(error: str, error_type: str = "Error") -> dict:
    """Create a standardized error response."""
    logger.error(f"{error_type}: {error}")
    return {"success": False, "data": None, "error": {"type": error_type, "message": error}}


def get_backups(noita_backup_helper: NoitaBackupHelper) -> dict:
    """Return all backups as serialized dicts."""
    try:
        result = noita_backup_helper.get_all_backups()
        backups = [backup.serialize() for backup in result]
        return _success_response(backups)
    except FileNotFoundError as e:
        return _error_response(str(e), "FileNotFoundError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def save_backup(noita_backup_helper: NoitaBackupHelper, backup_data: dict) -> dict:
    """Save a backup record and create a zip of the current save files.

    Expects backup_data to be a dict matching NoitaBackup.serialize() shape.
    Returns the saved backup as a serialized dict (including assigned id).
    """
    try:
        backup = NoitaBackup()
        backup.deserialize(backup_data)
        noita_backup_helper.save_backup(backup)
        return _success_response(backup.serialize())
    except FileNotFoundError as e:
        return _error_response(str(e), "FileNotFoundError")
    except ValueError as e:
        return _error_response(str(e), "ValueError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def delete_backup(noita_backup_helper: NoitaBackupHelper, backup_id: str) -> dict:
    """Delete the backup with the given id (removes record; zip file remains or is managed by helper)."""
    try:
        noita_backup_helper.delete_backup(backup_id)
        return _success_response()
    except FileNotFoundError as e:
        return _error_response(str(e), "FileNotFoundError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def load_backup(noita_backup_helper: NoitaBackupHelper, backup_id: str) -> dict:
    """Load the backup with the given id into the current Noita save directory."""
    try:
        noita_backup_helper.load_backup(backup_id)
        return _success_response()
    except FileNotFoundError as e:
        return _error_response(str(e), "FileNotFoundError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def duplicate_backup(
    noita_backup_helper: NoitaBackupHelper, backup_id: str, new_backup_data: dict | None = None
) -> dict:
    """Create a copy of an existing backup with a new ID.

    Args:
        noita_backup_helper: The backup helper instance
        backup_id: The ID of the backup to duplicate
        new_backup_data: Optional dict with new name/description/date for the duplicated backup

    Returns:
        Response dict with the newly created backup as a serialized dict
    """
    try:
        new_backup = noita_backup_helper.duplicate_backup(backup_id, new_backup_data)
        return _success_response(new_backup.serialize())
    except FileNotFoundError as e:
        return _error_response(str(e), "FileNotFoundError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def replace_backup(noita_backup_helper: NoitaBackupHelper, backup_id: str) -> dict:
    """Replace the backup files of the given backup ID with the current Noita save.

    Args:
        noita_backup_helper: The backup helper instance
        backup_id: The ID of the backup to replace

    Returns:
        Response dict with success or error status
    """
    try:
        noita_backup_helper.replace_backup(backup_id)
        return _success_response()
    except FileNotFoundError as e:
        return _error_response(str(e), "FileNotFoundError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def get_setting(key: str, default: Any = "") -> dict:
    """Retrieve a single setting value."""
    try:
        value = SettingHelper.get_setting(key, default)
        return _success_response(value)
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def save_setting(key: str, value: Any) -> dict:
    """Save a single setting key/value pair."""
    try:
        SettingHelper.save_setting(key, value)
        return _success_response()
    except OSError as e:
        return _error_response(str(e), "OSError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def save_settings(settings_data: dict) -> dict:
    """Save all settings from a dict."""
    try:
        SettingHelper.save_settings(settings_data)
        return _success_response()
    except OSError as e:
        return _error_response(str(e), "OSError")
    except TypeError as e:
        return _error_response(str(e), "TypeError")
    except Exception as e:
        return _error_response(str(e), type(e).__name__)


def get_all_settings() -> dict:
    """Return all settings as a dict."""
    try:
        settings = SettingHelper.load_settings()
        return _success_response(settings)
    except Exception as e:
        return _error_response(str(e), type(e).__name__)
