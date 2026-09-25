import os
from pathlib import Path

import yaml
from dotenv import load_dotenv


load_dotenv()


class ConfigReader:

    def __init__(self, environment="qa"):
        self.environment = environment

        config_path = (
            Path(__file__).resolve().parents[2]
            / "config"
            / "environments"
            / f"{environment}.yaml"
        )

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)

    def get(self, key):
        return self.config[key]

    def get_secret(self, key):
        value = os.getenv(key)

        if value is None:
            raise ValueError(
                f"Missing environment variable: {key}"
            )

        return value