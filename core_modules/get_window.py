import sys

if sys.platform == "win32":
    import ctypes
    import psutil

    from ctypes import wintypes


def get_window():
    if sys.platform == "win32":
        user32 = ctypes.windll.user32

        h_wnd = user32.GetForegroundWindow()
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))

        return psutil.Process(pid=pid.value).name().replace(".exe", "")

    # TODO else
