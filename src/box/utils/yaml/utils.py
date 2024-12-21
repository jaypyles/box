import yaml
from typing import Any
import os

DEFAULT_CONFIG_PATH = f"{os.getenv('HOME')}/.config/box"


def load_config(path: str) -> Any:
    os.makedirs(DEFAULT_CONFIG_PATH, exist_ok=True)

    if not os.path.exists(f"{DEFAULT_CONFIG_PATH}/{path}.yaml"):
        raise FileNotFoundError(
            f"Config file {DEFAULT_CONFIG_PATH}/{path}.yaml not found"
        )

    with open(f"{DEFAULT_CONFIG_PATH}/{path}.yaml", "r") as file:
        return yaml.safe_load(file)
