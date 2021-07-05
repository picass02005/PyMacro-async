import asyncio
import psutil

from global_modules import logs
from global_modules.temp_manager import purge_temp
from core_modules.tray import Tray

# ================================= Set the program priority below normal if possible ==================================
try:
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

except Exception as err:
    print(type(err), err)
# ======================================================================================================================

loop_ = asyncio.get_event_loop()
tray = None


async def main():
    global tray

    purge_temp_loop()

    while True:
        if isinstance(tray, Tray):
            print(tray.enabled)
            await asyncio.sleep(1)


def create_tray(loop: asyncio.AbstractEventLoop):
    global tray

    logs.info("main", "Launching tray")
    tray = Tray(loop)
    tray.run_tray()


def purge_temp_loop():
    purge_temp()

    loop = asyncio.get_running_loop()
    loop.call_later(60, purge_temp_loop)


purge_temp(True)
logs.clear_logs()

loop_.run_in_executor(None, create_tray, loop_)
loop_.create_task(main())
loop_.run_forever()
