import gc
import json
import importlib
import os
import sys

from global_modules import logs
from global_modules.get_config import get_config

__REGISTERED_PATH = f"{get_config('global.temp_dir')}/0-registered.json"


def __clear_registered():
    logs.info("module_manager", "Unloading all registered")
    with open(__REGISTERED_PATH, "w") as f:
        f.write("{}")


def register(window: str, key: str):
    """
    :param window: The window associated to the macro. Can be set to "default" to use it on every window if this hotkey isn't used for this window
    :param key: The hotkey associated to the macro
    :return: None
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)

            gc.collect()

            return None

        with open(__REGISTERED_PATH, "r") as f:
            actual_json = json.loads(f.read())

        if window not in actual_json.keys():
            actual_json.update({window: {}})

        if key in actual_json[window].keys():
            if actual_json[window][key] == f"{function.__module__}.{function.__name__}":
                return wrapper

        actual_json[window][key] = f"{function.__module__}.{function.__name__}"

        logs.info("macro_manager", f"Function {actual_json[window][key]} registered for window {window} and key {key}")

        with open(__REGISTERED_PATH, "w") as f:
            f.write(json.dumps(actual_json, indent=4))

        return wrapper

    return decorator


def load_all():
    for i in os.listdir("macros"):
        logs.info("macro_manager", f"Registering macros in macros/{i}/main")
        importlib.import_module(f"macros.{i}.main")
        del sys.modules[f"macros.{i}.main"]
        gc.collect()


def reload_all():
    __clear_registered()
    load_all()


def disable_all_macros_for_window(window: str):
    logs.info("macro_manager", f"Disabled all macros for window {window}")

    with open(__REGISTERED_PATH, "r") as f:
        actual_json = json.loads(f.read())

    actual_json[window] = None

    with open(__REGISTERED_PATH, "w") as f:
        f.write(json.dumps(actual_json, indent=4))
