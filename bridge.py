"""Bridge for python and frontend code to communicate"""

from noita_libs.noita_backup_helper import NoitaBackupHelper


def get_backups(noita_backup_helper: NoitaBackupHelper):
    result = noita_backup_helper.get_all_backups()

    return [backup.serialize() for backup in result]
