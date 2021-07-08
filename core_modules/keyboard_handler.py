import asyncio
from typing import Union

import keyboard
from pynput.keyboard import Key, KeyCode, Listener

from core_modules.macro_handler import MacroHandler
from core_modules.tray import Tray
from global_modules import logs


class KeyboardHandler:
    def __init__(self, macro_handler: MacroHandler, tray: Tray, loop: asyncio.AbstractEventLoop):
        self.__macro_handler = macro_handler
        self.__tray = tray
        self.__loop = loop

        self.__running = {}

        listener = Listener(on_press=self.__key_press_callback)
        listener.start()

    def __key_press_callback(self, key: Union[Key, KeyCode]):
        if not self.__tray.enabled:
            return

        key_universal = None

        if isinstance(key, Key):
            key_universal = key.name

        elif isinstance(key, KeyCode):
            if key.char is None:
                return

            else:
                key_universal = key.char

        if key_universal not in str(self.__macro_handler.actual_loaded.keys()):
            return

        for macro_key in self.__macro_handler.actual_loaded.keys():
            if self.__is_dict_key_pressed(macro_key):
                macro = self.__macro_handler.actual_loaded[macro_key]
                if macro['loop']:
                    key_running = f"{macro_key} {macro['callback']['location']}"
                    if key_running in self.__running.keys():
                        task = self.__running[key_running]['task']
                        task.cancel()
                        logs.info("keyboard_handler", f"Macro {macro['callback']['location']} stopped due to user "
                                                      f"input")
                        self.__running.pop(key_running)

                    else:
                        logs.info("keyboard_handler", f"Macro {macro['callback']['location']} running in loop")
                        task = self.__loop.create_task(self.__create_macro_loop_task_builder(macro['callback']['func']))
                        self.__running.update({key_running: {'task': task, 'location': macro['callback']['location']}})

                else:
                    self.__loop.create_task(self.__create_macro_task_builder(macro['callback']['func']))
                    logs.info("keyboard_handler", f"Macro {macro['callback']['location']} running")

    @staticmethod
    async def __create_macro_loop_task_builder(coro):
        while True:
            await coro()
            await asyncio.sleep(0)  # Needed or the program freeze

    @staticmethod
    async def __create_macro_task_builder(coro):
        await coro()

    @staticmethod
    def __is_dict_key_pressed(dict_key: str) -> bool:
        sub_keys = dict_key.split(".")

        for i in sub_keys:
            call = True
            for j in i.split("+"):
                if not keyboard.is_pressed(j):
                    call = False

            if call:
                return True

        return False

    def update(self):
        if self.__macro_handler.just_updated_loaded:
            self.__macro_handler.just_updated_loaded = False

            running_bkp = self.__running.copy()
            for key, item in running_bkp.items():
                task = self.__running[key]['task']
                task.cancel()
                logs.info("keyboard_handler", f"Macro {self.__running[key]['location']} stopped running due to window "
                                              f"change")
                self.__running.pop(key)
