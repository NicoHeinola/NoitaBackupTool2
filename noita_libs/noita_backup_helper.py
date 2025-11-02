import os
import uuid
import zipfile
from noita_libs.noita_backup import NoitaBackup
import json
import shutil


class NoitaBackupHelper:

    def __init__(self, noita_saves_dir_path: str, backup_dir_path: str, backup_filename: str) -> None:
        # Used for copying and replacing the current save file
        self._noita_saves_dir_path: str = noita_saves_dir_path
        self._save_dir_name: str = "save00"

        self._backups_dir_path: str = backup_dir_path
        self._backups_filename: str = backup_filename

    @property
    def current_noita_save_dir_path(self) -> str:
        return os.path.join(self._noita_saves_dir_path, self._save_dir_name)

    @property
    def backups_path(self) -> str:
        return os.path.join(self._backups_dir_path, self._backups_filename)

    @property
    def noita_saves_dir_path(self) -> str:
        return self._noita_saves_dir_path

    @property
    def backups_dir_path(self) -> str:
        return self._backups_dir_path

    @property
    def backups_filename(self) -> str:
        return self._backups_filename

    @backups_filename.setter
    def backups_filename(self, value: str | None) -> None:
        if value is None:
            value = ""
            return

        self._backups_filename = value

    @backups_dir_path.setter
    def backups_dir_path(self, value: str | None) -> None:
        if value is None:
            value = ""
            return

        self._backups_dir_path = value

    @noita_saves_dir_path.setter
    def noita_saves_dir_path(self, value: str | None) -> None:
        if value is None:
            value = ""
            return

        self._noita_saves_dir_path = value

    def get_backup_file_path(self, backup_id: str) -> str:
        return os.path.join(self._backups_dir_path, f"backup_{backup_id}.zip")

    def _backup_current_save_file(self, backup_id: str) -> None:
        # Make sure noita save directory exists
        if not os.path.exists(self.current_noita_save_dir_path):
            raise FileNotFoundError(f"Noita save directory does not exist at {self.current_noita_save_dir_path}.")

        backup_save_file_path = self.get_backup_file_path(backup_id)

        # Remove an existing backup file with the same id
        if os.path.exists(backup_save_file_path):
            os.remove(backup_save_file_path)

        # Create the backups directory if it doesn't exist
        os.makedirs(self._backups_dir_path, exist_ok=True)

        # Create a zip archive of the entire save directory
        with zipfile.ZipFile(backup_save_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.current_noita_save_dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.current_noita_save_dir_path)
                    zipf.write(file_path, arcname)

    def load_backup(self, backup_id: str) -> None:
        # Make sure noita save directory exists
        if not os.path.exists(self._noita_saves_dir_path):
            raise FileNotFoundError(f"Noita save directory does not exist at {self._noita_saves_dir_path}.")

        backup_save_file_path = self.get_backup_file_path(backup_id)

        if not os.path.exists(backup_save_file_path):
            raise FileNotFoundError(f"Backup file with ID {backup_id} does not exist.")

        # Clear the current save directory
        if os.path.exists(self.current_noita_save_dir_path):
            shutil.rmtree(self.current_noita_save_dir_path)

        # Create the folder
        os.makedirs(self.current_noita_save_dir_path)

        # Extract the backup zip file to the current save directory
        with zipfile.ZipFile(backup_save_file_path, "r") as zip_ref:
            zip_ref.extractall(self.current_noita_save_dir_path)

    def get_all_backups(self) -> list[NoitaBackup]:
        backups: list[NoitaBackup] = []

        if not os.path.exists(self.backups_path):
            return backups

        with open(self.backups_path, "r+", encoding="utf-8") as backups_file:
            backups_data = json.load(backups_file)

            for backup_data in backups_data:
                backup = NoitaBackup()
                backup.deserialize(backup_data)

                backups.append(backup)

        return backups

    def save_all_backups(self, backups: list[NoitaBackup]) -> None:
        backups_data: list[dict] = []

        for backup in backups:
            backups_data.append(backup.serialize())

        with open(self.backups_path, "w+", encoding="utf-8") as backups_file:
            json.dump(backups_data, backups_file, indent=4)

    def save_backup(self, backup: NoitaBackup) -> None:
        backups = self.get_all_backups()

        # Check if backup with the same ID already exists
        for i, existing_backup in enumerate(backups):
            if existing_backup.id == backup.id:
                backups[i] = backup
                break
        else:
            # Create a random ID for the new backup
            backup.id = str(uuid.uuid4())
            backups.append(backup)

            # Backup the current save file
            self._backup_current_save_file(backup.id)

        self.save_all_backups(backups)

    def delete_backup(self, backup_id: str) -> None:
        backups = self.get_all_backups()

        # Remove from disk
        backup_save_file_path = self.get_backup_file_path(backup_id)
        if os.path.exists(backup_save_file_path):
            os.remove(backup_save_file_path)

        # Remove backup with the given ID
        backups = [backup for backup in backups if backup.id != backup_id]

        self.save_all_backups(backups)

    def duplicate_backup(self, backup_id: str, new_backup_data: dict | None = None) -> NoitaBackup:
        """Create a copy of an existing backup with a new ID.

        Args:
            backup_id: The ID of the backup to duplicate
            new_backup_data: Optional dict with new name/description/date for the duplicated backup

        Returns:
            The newly created backup

        Raises:
            FileNotFoundError: If the backup doesn't exist
        """
        backups = self.get_all_backups()

        # Find the backup to duplicate
        backup_to_duplicate = None
        for backup in backups:
            if backup.id == backup_id:
                backup_to_duplicate = backup
                break

        if backup_to_duplicate is None:
            raise FileNotFoundError(f"Backup with ID {backup_id} does not exist.")

        # Check if the zip file exists
        backup_save_file_path = self.get_backup_file_path(backup_id)
        if not os.path.exists(backup_save_file_path):
            raise FileNotFoundError(f"Backup file for ID {backup_id} does not exist.")

        # Create new backup record
        new_backup = NoitaBackup()
        new_backup.id = str(uuid.uuid4())

        new_backup.deserialize(backup_to_duplicate.serialize())
        if new_backup_data is not None:
            new_backup.deserialize(new_backup_data)

        # Copy the zip file
        new_backup_file_path = self.get_backup_file_path(new_backup.id)
        shutil.copy2(backup_save_file_path, new_backup_file_path)

        # Add to backups list and save
        backups.append(new_backup)
        self.save_all_backups(backups)

        return new_backup

    def replace_backup(self, backup_id: str) -> None:
        """Replace the backup files of the given backup ID with the current Noita save.

        Args:
            backup_id: The ID of the backup to replace

        Raises:
            FileNotFoundError: If the backup doesn't exist
        """
        backups = self.get_all_backups()

        # Check if backup exists
        backup_exists = any(backup.id == backup_id for backup in backups)
        if not backup_exists:
            raise FileNotFoundError(f"Backup with ID {backup_id} does not exist.")

        # Delete the old backup file
        backup_save_file_path = self.get_backup_file_path(backup_id)
        if os.path.exists(backup_save_file_path):
            os.remove(backup_save_file_path)

        # Create new backup file with current save
        self._backup_current_save_file(backup_id)
