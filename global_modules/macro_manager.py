import asyncio
import gc
import importlib
import json
import os
import sys
from typing import Callable
from typing import List
from typing import Union
from typing import Coroutine

from global_modules import logs
from global_modules.get_config import get_config

REGISTERED_PATH = f"{get_config('global.temp_dir')}/0-registered.json"


def __clear_registered() -> None:
    """
    :return: None
    """

    logs.info("macro_manager", "Unloading all registered")
    with open(REGISTERED_PATH, "w") as f:
        f.write("{}")


def register(
        window: Union[str, List[str]],
        key: str, loop: bool = False,
        before: Union[None, Callable] = None,
        after: Union[None, Callable] = None
) -> Union[None, Callable]:

    """
    :param window: The window associated to the macro. Can be set to "default" to use it on every window if this
    hotkey isn't used for this window. Can be a list to allow multiple window
    :param key: The hotkey associated to the macro. '.' mean OR and '+' mean AND
    :param loop: Set it to True if you want your macro to loop until you press a 2nd time the key
    :param before: A coroutine which will run once before the macro (can be set to None)
    :param after: A coroutine which will run once after the macro (can be set to None)
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
                if actual_json[w][l_key] == __create_entry(function, loop, before, after):
                    return wrapper

            else:
                if __check_coroutines(function, before, after):
                    actual_json[w][l_key] = __create_entry(function, loop, before, after)
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
    try:
        load_all()
    except Exception as err: print(type(err), err)


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


def __create_entry(
        callback: Coroutine,
        loop: bool,
        before: Union[Coroutine, None],
        after: Union[Coroutine, None]
) -> dict:

    return {
        "after": f"{after.__module__}.{after.__name__}" if after is not None else None,
        "before": f"{before.__module__}.{before.__name__}" if before is not None else None,
        "callback": f"{callback.__module__}.{callback.__name__}",
        "loop": loop,
    }


def __check_coroutines(function, before, after):
    to_add = True
    if not asyncio.iscoroutinefunction(function):
        logs.error("macro_manager",
                   f"Macro defined at {function.__module__}.{function.__name__} isn't a coroutine. Define "
                   f"it with 'async def'")
        to_add = False

    if not asyncio.iscoroutinefunction(before) and before is not None:
        logs.error("macro_manager",
                   f"Before defined at {before.__module__}.{before.__name__} isn't a coroutine. Define it with 'async "
                   f"def'")
        to_add = False

    if not asyncio.iscoroutinefunction(after) and after is not None:
        logs.error("macro_manager",
                   f"After defined at {after.__module__}.{after.__name__} isn't a coroutine. Define it with 'async "
                   f"def'")
        to_add = False

    return to_add

