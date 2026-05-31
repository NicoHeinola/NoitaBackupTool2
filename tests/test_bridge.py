import os
import sys
from pathlib import Path

# Ensure project root is on sys.path for imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from bridge import status
from noita_libs.noita_backup_helper import NoitaBackupHelper
from setting_libs.setting_helper import SettingHelper


def test_bridge_status(tmp_path, monkeypatch):
    # Prepare directories
    saves_dir = tmp_path / "saves"
    backups_dir = tmp_path / "backups"
    saves_dir.mkdir()
    backups_dir.mkdir()

    # create save00 with one file
    save00 = saves_dir / "save00"
    save00.mkdir()
    (save00 / "a.txt").write_text("x")

    # create a backups json file with content
    backups_file = backups_dir / "backups.json"
    backups_file.write_text("[]")

    helper = NoitaBackupHelper(str(saves_dir), str(backups_dir), "backups.json")

    resp = status(helper)
    assert resp.get("success") is True
    data = resp.get("data")
    assert data is not None
    assert data["noita_save_exists"] is True
    assert data["noita_save_not_empty"] is True
    assert data["backups_dir_exists"] is True
    assert data["backups_dir_not_empty"] is True
    assert data["backups_file_exists"] is True
