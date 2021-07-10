import asyncio
import gc
import os

import psutil
import sys

from core_modules.keyboard_handler import KeyboardHandler
from core_modules.macro_handler import MacroHandler
from core_modules.tray import Tray
from global_modules import logs
from global_modules.get_config import get_config
from global_modules.macro_manager import __clear_registered, load_all
from global_modules.temp_manager import purge_temp

# ================================= Set the program priority below normal if possible ==================================
if sys.platform == "win32":
    try:
        psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

    except Exception as err:
        logs.error("core", f"Cannot set process priority below normal: {type(err)}: {err}")

elif sys.platform == "linux" or sys.platform == "linux2":
    try:
        psutil.Process().nice(10)
    except Exception as err:
        logs.error("core", f"Cannot set nice to 10: {type(err)}: {err}")
# ======================================================================================================================

loop_ = asyncio.get_event_loop()
tray = None
macro_handler = None
keyboard_handler = None


async def main():
    global tray
    global macro_handler
    global keyboard_handler

    purge_temp_loop()

    while not isinstance(tray, Tray):
        await asyncio.sleep(0.1)

    if isinstance(tray, Tray):
        macro_handler = MacroHandler(tray)
        keyboard_handler = KeyboardHandler(macro_handler, tray, asyncio.get_event_loop())

    update_handlers_loop()

    gc.collect()


def create_tray(loop: asyncio.AbstractEventLoop):
    global tray

    logs.info("main", "Launching tray")
    tray = Tray(loop)
    tray.run_tray()


def purge_temp_loop():
    purge_temp()

    loop = asyncio.get_running_loop()
    loop.call_later(60, purge_temp_loop)


def update_handlers_loop():
    global macro_handler
    global keyboard_handler
    global tray

    if isinstance(tray, Tray):
        if tray.enabled:
            to = get_config("global.timeout_update_handler.enabled")
        else:
            to = get_config("global.timeout_update_handler.disabled")

    else:
        to = get_config("global.timeout_update_handler.enabled")

    if isinstance(macro_handler, MacroHandler):
        macro_handler.update()

    if isinstance(keyboard_handler, KeyboardHandler):
        keyboard_handler.update()

    loop = asyncio.get_running_loop()
    loop.call_later(to, update_handlers_loop)


if __name__ == "__main__":
    if sys.platform == "darwin":
        logs.error("core", "MacOS not supported")
        exit(1)

    if not os.path.exists("macros"):
        os.mkdir("macros")

    purge_temp(True)
    logs.clear_logs()
    __clear_registered()
    load_all()

    loop_.run_in_executor(None, create_tray, loop_)
    loop_.create_task(main())
    loop_.run_forever()
