import asyncio
import gc
import importlib
import json
import os
import sys
from typing import Callable
from typing import Union, List

from global_modules import logs
from global_modules.get_config import get_config

REGISTERED_PATH = f"{get_config('global.temp_dir')}/0-registered.json"


def __clear_registered() -> None:
    """
    :return: None
    """

    logs.info("module_manager", "Unloading all registered")
    with open(REGISTERED_PATH, "w") as f:
        f.write("{}")


def register(window: Union[str, List[str]], key: str, loop: bool = False) -> Union[None, Callable]:
    """
    :param window: The window associated to the macro. Can be set to "default" to use it on every window if this
    hotkey isn't used for this window. Can be a list to allow multiple window
    :param key: The hotkey associated to the macro. '.' mean OR and '+' mean AND
    :param loop: Set it to True if you want your macro to loop until you press a 2nd time the key
    :return: None
    """

    def decorator(function):
        async def wrapper(*args, **kwargs):
            await function(*args, **kwargs)

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

            l_key = key.lower()
            if l_key in actual_json[w].keys():
                if actual_json[w][l_key] == {"callback": f"{function.__module__}.{function.__name__}", "loop": loop}:
                    return wrapper

            if not asyncio.iscoroutinefunction(function):
                logs.error("macro_manager", f"Macro defined at {function.__module__}.{function.__name__} isn't a "
                                            f"coroutine. Define it with 'async def'")
            else:
                actual_json[w][l_key] = {"callback": f"{function.__module__}.{function.__name__}", "loop": loop}
                logs.info("macro_manager", f"Function {actual_json[w][l_key]} registered for window {w} and key "
                                           f"{l_key}")

        with open(REGISTERED_PATH, "w") as f:
            f.write(json.dumps(actual_json, indent=4))

        return wrapper

    return decorator


def load_all() -> None:
    """
    :return: None
    """

    logs.info("macro_manager", f"{'='*10} Registering macros {'='*10}")
    for i in os.listdir("macros"):
        logs.info("macro_manager", f"--- Registering macros in macros/{i}/main.py ---")
        module = importlib.import_module(f"macros.{i}.main")
        importlib.reload(module)
        del sys.modules[f"macros.{i}.main"]
        gc.collect()
    logs.info("macro_manager", '='*40)


def reload_all() -> None:
    """
    :return: None
    """

    __clear_registered()
    load_all()


def disable_all_macros_for_window(window: str) -> None:
    """
    :param window: The window you want to disable all macros
    :return: None
    """

    with open(REGISTERED_PATH, "r") as f:
        actual_json = json.loads(f.read())

    if window in actual_json.keys():
        if actual_json[window] is None:
            return

    logs.info("macro_manager", f"Disabled all macros for window {window}")

    actual_json[window] = None

    with open(REGISTERED_PATH, "w") as f:
        f.write(json.dumps(actual_json, indent=4))
