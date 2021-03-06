import gc
import importlib
import json
from typing import Coroutine, Union

from core_modules.get_window import get_window
from core_modules.tray import Tray
from global_modules import logs


class MacroHandler:
    def __init__(self, tray: Tray):
        from global_modules.macro_manager import REGISTERED_PATH
        self.__REGISTERED_PATH = REGISTERED_PATH

        self.__tray = tray
        self.__window_name = get_window()

        self.actual_loaded = {}
        self.just_updated_loaded = False  # A variable for the keyboard_handler

        logs.info("macro_handler", f"Loading macros for window {self.__window_name}")
        self.__update_registered_for_window()

    def __update_registered_for_window(self):
        with open(self.__REGISTERED_PATH, "r") as f:
            actual_json = json.loads(f.read())

        actual_loaded = {}

        if "default" in actual_json.keys():
            actual_loaded.update(actual_json["default"].items())

        for i in actual_json.keys():
            if i.lower() in self.__window_name.lower():
                if actual_json[i] is None:
                    self.actual_loaded = {}
                    return
                else:
                    actual_loaded.update(actual_json[i].items())

        tmp = {}
        for key, value in actual_loaded.items():
            try:
                module = importlib.import_module(".".join(value['callback'].split(".")[:-1]))
                importlib.reload(module)

            except ModuleNotFoundError:
                return logs.error("macro_handler", f"Module {'.'.join(value['callback'].split('.')[:-1])} not found")

            try:
                callback = eval(f"module.{value['callback'].split('.')[-1]}")

            except AttributeError:
                return logs.error("macro_handler", f"Function {value['callback']} not found")

            callback = self.__get_callback_from_location(value['callback'])
            before = self.__get_callback_from_location(value['before']) if value['before'] is not None else None
            after = self.__get_callback_from_location(value['after']) if value['after'] is not None else None

            if callback is not None:
                tmp.update({key: {
                    'callback': {"func": callback, "location": value['callback']},
                    'before': {"func": before, "location": value['before']},
                    'after': {"func": after, "location": value['after']},
                    'loop': value['loop']}
                })

        self.actual_loaded = {}
        self.actual_loaded.update(tmp)
        self.just_updated_loaded = True

    def update(self):
        if not self.__tray.enabled:
            if self.actual_loaded:
                self.actual_loaded = {}
                self.__window_name = None
                logs.info("macro_handler", "Actually loaded cleared")
                return

        if self.__window_name != (window := get_window()):
            logs.info("macro_handler", f"Window changed from {self.__window_name} to {window}, reloading macros...")
            self.__window_name = window
            self.__update_registered_for_window()

            gc.collect()

    @staticmethod
    def __get_callback_from_location(location) -> Union[Coroutine, None]:
        try:
            module = importlib.import_module(".".join(location.split(".")[:-1]))
            importlib.reload(module)

        except ModuleNotFoundError:
            return logs.error("macro_handler", f"Module {'.'.join(location.split('.')[:-1])} not found")

        try:
            return eval(f"module.{location.split('.')[-1]}")

        except AttributeError:
            return logs.error("macro_handler", f"Function {location} not found")
