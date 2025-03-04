import os
import json

class ConfigService:
    def __init__(self):
        pass

    # Build the path to plugin_config.json
    CONFIG_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "plugin_config.json"
    )

    @staticmethod
    def load_config():
        with open(ConfigService.CONFIG_PATH, "r") as f:
            return json.load(f)

    @staticmethod
    def get_file_formats():
        config = ConfigService.load_config()
        return config.get("file_formats", [])

    @staticmethod
    def get_version():
        config = ConfigService.load_config()
        return config.get("version", "")