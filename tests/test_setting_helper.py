import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from setting_libs.setting_helper import SettingHelper


def test_save_and_load_settings(tmp_path, monkeypatch):
    settings_file = tmp_path / "settings.json"
    monkeypatch.setattr(SettingHelper, "setting_file_path", str(settings_file))

    # Initially empty
    assert SettingHelper.load_settings() == {}

    # Save settings
    data = {"a": "1", "b": "2"}
    SettingHelper.save_settings(data)

    # File should exist and load the same data
    loaded = SettingHelper.load_settings()
    assert loaded == data

    # get_setting with default
    assert SettingHelper.get_setting("a") == "1"
    assert SettingHelper.get_setting("missing", "x") == "x"

    # save_setting updates file
    SettingHelper.save_setting("c", "3")
    assert SettingHelper.get_setting("c") == "3"
