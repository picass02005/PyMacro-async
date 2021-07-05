import time


def info(module: str, log: str):
    __add_log(module, "INFO", log)


def warn(module: str, log: str):
    __add_log(module, "WARN", log)


def error(module: str, log: str):
    __add_log(module, "ERROR", log)


def __add_log(module: str, level: str, log: str):
    log_ = f"[{time.strftime('%H:%M:%S')}] [{module}/{level}] {log}"
    with open("latest.log", "a") as f:
        f.write(f"{log_}\n")
    print(log_)


def clear_logs():
    with open("latest.log", "w") as f:
        pass
