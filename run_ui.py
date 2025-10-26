from setting_libs.setting_helper import SettingHelper
from noita_libs.noita_backup_helper import NoitaBackupHelper
from ui_libs.ui import launch


def main():
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

    # Launch the UI
    launch(noita_backup_helper)


if __name__ == "__main__":
    main()
