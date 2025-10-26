from noita_libs.noita_backup import NoitaBackup
from noita_libs.noita_backup_helper import NoitaBackupHelper
from setting_libs.setting_helper import SettingHelper


if __name__ == "__main__":
    noita_saves_dir_path: str = SettingHelper.get_setting(
        "noita_saves_dir_path", "/mnt/c/Users/user/AppData/LocalLow/Nolla_Games_Noita"
    )
    backup_dir_path: str = SettingHelper.get_setting("backup_dir_path", "./data/backups")
    backup_filename: str = SettingHelper.get_setting("backup_filename", "backups.json")

    noita_backup_helper: NoitaBackupHelper = NoitaBackupHelper(
        noita_saves_dir_path=noita_saves_dir_path,
        backup_dir_path=backup_dir_path,
        backup_filename=backup_filename,
    )

    SettingHelper.save_setting("noita_saves_dir_path", noita_saves_dir_path)
    SettingHelper.save_setting("backup_dir_path", backup_dir_path)
    SettingHelper.save_setting("backup_filename", backup_filename)

    new_backup: NoitaBackup = NoitaBackup(
        name="Test 1",
        description="This is a test backup",
        date="2024-06-15",
    )

    # noita_backup_helper.save_backup(new_backup)

    list_of_backups: list[NoitaBackup] = noita_backup_helper.get_all_backups()

    noita_backup_helper.load_backup(list_of_backups[0].id)
