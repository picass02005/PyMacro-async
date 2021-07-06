import gc
import json
import importlib
import os
import sys
from typing import Union, List

from global_modules import logs
from global_modules.get_config import get_config

REGISTERED_PATH = f"{get_config('global.temp_dir')}/0-registered.json"


def __clear_registered():
    logs.info("module_manager", "Unloading all registered")
    with open(REGISTERED_PATH, "w") as f:
        f.write("{}")


def register(window: Union[str, List[str]], key: str):
    """
    :param window: The window associated to the macro. Can be set to "default" to use it on every window if this
    hotkey isn't used for this window. Can be a list to allow multiple window
    :param key: The hotkey associated to the macro
    :return: None
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)

            gc.collect()

            return None

        with open(REGISTERED_PATH, "r") as f:
            actual_json = json.loads(f.read())

        if isinstance(window, str):
            windows = [window]

        else:
            windows = window

        for w in windows:
            if w not in actual_json.keys():
                actual_json.update({w: {}})

            if key in actual_json[w].keys():
                if actual_json[w][key] == f"{function.__module__}.{function.__name__}":
                    return wrapper

            actual_json[w][key] = f"{function.__module__}.{function.__name__}"

            logs.info("macro_manager", f"Function {actual_json[w][key]} registered for window {w} and key {key}")

        with open(REGISTERED_PATH, "w") as f:
            f.write(json.dumps(actual_json, indent=4))

        return wrapper

    return decorator


def load_all():
    logs.info("macro_manager", f"{'='*10} Registering macros {'='*10}")
    for i in os.listdir("macros"):
        logs.info("macro_manager", f"--- Registering macros in macros/{i}/main.py ---")
        module = importlib.import_module(f"macros.{i}.main")
        importlib.reload(module)
        del sys.modules[f"macros.{i}.main"]
        gc.collect()
    logs.info("macro_manager", '='*40)


def reload_all():
    __clear_registered()
    load_all()


def disable_all_macros_for_window(window: str):
    with open(REGISTERED_PATH, "r") as f:
        actual_json = json.loads(f.read())

    if window in actual_json.keys():
        if actual_json[window] is None:
            return

    logs.info("macro_manager", f"Disabled all macros for window {window}")

    actual_json[window] = None

    with open(REGISTERED_PATH, "w") as f:
        f.write(json.dumps(actual_json, indent=4))
