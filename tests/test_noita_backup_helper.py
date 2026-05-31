import os
import sys
import zipfile
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from noita_libs.noita_backup_helper import NoitaBackupHelper
from noita_libs.noita_backup import NoitaBackup


def test_path_checks_and_backup_prevention(tmp_path):
    # Setup base dirs
    base = tmp_path / "noita"
    saves_dir = base / "saves"
    backups_dir = base / "backups"
    saves_dir.mkdir(parents=True)
    backups_dir.mkdir(parents=True)

    # No save00 -> noita_save_path_exists should be False
    helper = NoitaBackupHelper(str(saves_dir), str(backups_dir), "backups.json")
    assert not helper.noita_save_path_exists()
    assert not helper.path_not_empty(helper.current_noita_save_dir_path)

    # Create save00 but empty -> exists True but not_empty False
    save00 = saves_dir / "save00"
    save00.mkdir()
    assert helper.noita_save_path_exists()
    assert not helper.path_not_empty(helper.current_noita_save_dir_path)

    # Attempting to backup empty folder should raise
    try:
        helper._backup_current_save_file("testid")
        raise AssertionError("Expected ValueError when backing up empty folder")
    except ValueError:
        pass

    # Add a file and perform backup
    (save00 / "file.txt").write_text("hello")
    assert helper.path_not_empty(helper.current_noita_save_dir_path)

    # Ensure backups dir exists and is empty
    assert helper.backups_dir_exists()

    # Call _backup_current_save_file directly
    helper._backup_current_save_file("testid")
    backup_file = helper.get_backup_file_path("testid")
    assert os.path.exists(backup_file)
    # zip should contain the file
    with zipfile.ZipFile(backup_file, "r") as z:
        assert any(n.endswith("file.txt") for n in z.namelist())


def test_load_backup_refuses_empty_archive(tmp_path):
    base = tmp_path / "noita2"
    saves_dir = base / "saves"
    backups_dir = base / "backups"
    saves_dir.mkdir(parents=True)
    backups_dir.mkdir(parents=True)

    helper = NoitaBackupHelper(str(saves_dir), str(backups_dir), "backups.json")

    # Create an empty backup file (zero bytes)
    empty_backup = backups_dir / "backup_empty.zip"
    empty_backup.write_bytes(b"")

    # Attempt to load should raise ValueError
    try:
        helper.load_backup("empty")
        raise AssertionError("Expected FileNotFoundError or ValueError for empty backup")
    except (ValueError, FileNotFoundError):
        pass

    # Create a zip with no files inside
    zip_path = backups_dir / "backup_nofiles.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        # create an archive but add no entries
        pass

    # Rename to expected backup id name
    os.rename(str(zip_path), helper.get_backup_file_path("nofiles"))

    try:
        helper.load_backup("nofiles")
        raise AssertionError("Expected ValueError for archive with no files")
    except ValueError:
        pass
