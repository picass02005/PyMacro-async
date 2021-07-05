import sys
import time

from global_modules.get_config import get_config

LOG_PATH = f"{get_config('global.temp_dir')}/0-latest.log"


def info(module: str, log: str):
    __add_log(module, "INFO", log)


def warn(module: str, log: str):
    __add_log(module, "WARN", log)


def error(module: str, log: str):
    __add_log(module, "ERROR", log, True)


def __add_log(module: str, level: str, log: str, error_pipe: bool = False):
    log_ = f"[{time.strftime('%H:%M:%S')}] [{module}/{level}] {log}"
    with open(LOG_PATH, "a") as f:
        f.write(f"{log_}\n")

    if not error_pipe:
        print(log_)

    else:
        print(log_, file=sys.stderr)


def clear_logs():
    with open(LOG_PATH, "w"):
        pass
