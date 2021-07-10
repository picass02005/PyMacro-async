import sys
import psutil

from global_modules import logs

if sys.platform == "win32":
    import ctypes

    from ctypes import wintypes

elif sys.platform == "linux" or sys.platform == "linux2":
    import subprocess

    proc = subprocess.Popen(["/bin/bash", "-c", "which xdotool"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_, stderr_ = proc.communicate()
    if stderr_:
        logs.error("get_window", f"Cannot find xdotool. Please install it with apt / pacman / dnf / ... "
                                 f"(bash error: {stderr_.decode()[:-1]})")
        exit(1)

    else:
        path = stdout_.decode()[:-1]
        logs.info("get_window", f"xdotool found under {path}")


def get_window():
    if sys.platform == "win32":
        user32 = ctypes.windll.user32

        h_wnd = user32.GetForegroundWindow()
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))

        return psutil.Process(pid=pid.value).name().replace(".exe", "")

    else:
        process = subprocess.Popen([path, "getactivewindow", "getwindowpid"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr:
            logs.error("get_window", f"Active window pid not found: (${path} getactivewindow getwindowpid) >& "
                                     f"{stderr.decode()[:-1]}")

            return None

        else:
            pid = int(stdout.decode()[:-1])
            return psutil.Process(pid=pid).exe()
