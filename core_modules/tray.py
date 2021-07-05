import asyncio
import os
import subprocess
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from global_modules import logs


class Tray:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop

        self.__app = QApplication([])
        self.__app.setQuitOnLastWindowClosed(False)
        self.__parent = QWidget()
        self.__icon = QIcon("tray_image/tray_enabled.png")

        self.tray = QSystemTrayIcon(self.__icon, self.__parent)
        self.tray.setToolTip("PyMacro")

        self.enabled = True

        self.__build_menu(enabled=True)

        self.tray.setVisible(True)

    def __build_menu(self, enabled: bool = True):
        menu = QMenu(self.__parent)

        item = QAction(self.__parent)
        item.setText("PyMacro - By picasso2005")
        item.setEnabled(False)
        menu.addAction(item)

        if enabled:
            item = QAction(self.__parent)
            item.setText("Disable")
            item.triggered.connect(lambda: self.__toggle_enabled())

        else:
            item = QAction(self.__parent)
            item.setText("Enable")
            item.triggered.connect(lambda: self.__toggle_enabled())

        menu.addAction(item)

        item = QAction(self.__parent)
        item.setText("Open macros folder")
        item.triggered.connect(lambda: self.__open_folder())
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setText("Open logs")
        item.triggered.connect(lambda: self.__open_logs())
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setText("Exit")
        item.triggered.connect(lambda: self.__exit())
        menu.addAction(item)

        self.tray.setContextMenu(menu)

    def run_tray(self):
        self.__app.exec_()

    def __toggle_enabled(self):
        if self.enabled:
            self.enabled = False
            self.tray.setIcon(QIcon("tray_image/tray_disabled.png"))
            self.__build_menu(enabled=False)

            logs.info("tray", "Macros disabled")

        else:
            self.enabled = True
            self.tray.setIcon(QIcon("tray_image/tray_enabled.png"))
            self.__build_menu(enabled=True)

            logs.info("tray", "Macros enabled")

    @staticmethod
    def __open_logs():
        if sys.platform == "win32":
            subprocess.Popen(f"\"{os.getcwd()}\\{logs.LOG_PATH}\"", shell=True)

        #  TODO FOR OTHER OS

    @staticmethod
    def __open_folder():
        if sys.platform == "win32":
            subprocess.Popen(f"explorer \"{os.getcwd()}\\macros\"", shell=True)

        #  TODO FOR OTHER OS

    def __exit(self):
        self.__app.exit(0)
        self.loop.stop()

        logs.info("tray", "Exiting app")

        exit(0)
