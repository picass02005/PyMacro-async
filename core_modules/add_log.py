import os
import time

path = os.getcwd() + os.sep + "latest.log"


def add_log(category: str, log: str) -> None:
    """
    :param category: The category of the log.
    :param log: The log
    :return: None
    """

    with open(path, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] [{category}] {log}\n")

    print(f"[{time.strftime('%H:%M:%S')}] [{category}] {log}")


def reset_logs():
    with open(path, "w"):
        pass
