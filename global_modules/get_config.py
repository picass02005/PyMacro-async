import json
import os
from typing import Any


def get_config(config_key: str) -> Any:
    """
    :param config_key: The name of the config you want to get, use . as separators to get sub config
    :return: The data
    """

    module = config_key.split(".")[0]
    config_key = config_key.split(".")[1:]

    if module == "global":
        with open(f"config.json", "r") as f:
            config = json.load(f)

    else:
        with open(f"macros{os.sep}{module}{os.sep}config.json", "r") as f:
            config = json.load(f)

    while config_key:
        config = config[config_key[0]]
        config_key.pop(0)

    return config
