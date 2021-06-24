import asyncio
import psutil

from global_modules.temp_manager import purge_temp
from tray import Tray

# ================================= Set the program priority below normal if possible ==================================
try:
    psutil.Process().nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

except:
    pass
# ======================================================================================================================


async def main():
    purge_temp_loop()

    Tray()


def purge_temp_loop():
    purge_temp()

    loop_ = asyncio.get_event_loop()
    loop_.call_later(60, purge_temp_loop)


purge_temp(True)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
