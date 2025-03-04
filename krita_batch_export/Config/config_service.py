import os
import json

# FIXME: Strictly speaking, this class is a service and should be in the Logic folder but it kinda makes sense to keep it here

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