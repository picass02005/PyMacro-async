import asyncio
import json
import os
import subprocess
import sys

import pystray
from PIL import Image
from pystray import MenuItem

from global_modules import temp_manager


class Tray:
    def __init__(self, loop: asyncio.ProactorEventLoop):
        self.json_path = temp_manager.create_random_file(base_name="status", extension="json", time_=0)
        self.loop = loop

        with open(self.json_path, "w") as f:
            f.write(json.dumps({'activated': True}, indent=4))

        self.icon = None

        self.create_tray(True)

    def create_tray(self, enabled: bool):
        if enabled:
            image = "tray_image/tray_enabled.png"
            menu_item = 'Disable'

        else:
            image = "tray_image/tray_disabled.png"
            menu_item = 'Enable'

        image = Image.open(image)
        menu_items = [
            MenuItem('PyMacro', lambda: None, enabled=False),
            MenuItem(menu_item, lambda: self.__toggle_activated()),
            MenuItem('Open logs', lambda: subprocess.call(f"\"{os.getcwd()}\\latest.log\"", shell=True)),
            MenuItem('Exit', self.__close)
        ]

        if sys.platform == "win32":
            menu_items.insert(2, MenuItem('Open macros folder',
                                          lambda: subprocess.call(f"explorer \"{os.getcwd()}\\macros\"", shell=True)))

        menu = pystray.Menu(*tuple(menu_items))

        if self.icon is None:
            self.icon = pystray.Icon("PyMacro", image, "PyMacro - By picasso2005", menu)

            self.icon.run()

        else:
            self.icon.icon = image
            self.icon.menu = menu

    def __toggle_activated(self):
        with open(self.json_path, "r") as f:
            activated = json.loads(f.read())['activated']

        if activated:
            with open(self.json_path, "w") as f:
                f.write(json.dumps({'activated': False}, indent=4))

            self.create_tray(False)

        else:
            with open(self.json_path, "w") as f:
                f.write(json.dumps({'activated': True}, indent=4))

            self.create_tray(True)

    def __close(self):
        self.icon.stop()
        self.loop.stop()
