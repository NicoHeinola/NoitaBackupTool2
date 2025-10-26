import json
import os


class SettingHelper:
    setting_file_path: str = os.path.join("data/settings", "settings.json")

    @staticmethod
    def load_settings() -> dict:
        if not os.path.exists(SettingHelper.setting_file_path):
            return {}

        with open(SettingHelper.setting_file_path, "r", encoding="utf-8") as settings_file:
            settings_data = json.load(settings_file)

        return settings_data

    @staticmethod
    def save_settings(settings_data: dict) -> None:
        if not os.path.exists(os.path.dirname(SettingHelper.setting_file_path)):
            os.makedirs(os.path.dirname(SettingHelper.setting_file_path))

        with open(SettingHelper.setting_file_path, "w+", encoding="utf-8") as settings_file:
            json.dump(settings_data, settings_file, indent=4)

    @staticmethod
    def save_setting(key: str, value: str) -> None:
        settings: dict = SettingHelper.load_settings()
        settings[key] = value
        SettingHelper.save_settings(settings)

    @staticmethod
    def get_setting(key: str, default_value="") -> str:
        settings: dict = SettingHelper.load_settings()

        return settings.get(key, default_value)
