import os
import random
import shutil
import string
import time

from global_modules import logs
from global_modules.get_config import get_config

if not os.path.isdir(get_config("global.temp_dir")):
    os.mkdir(get_config("global.temp_dir"))


def __create_random_string(length: int = 32, contain_digits: bool = False) -> str:
    """
    :param length: The length of the random string
    :param contain_digits: If set to True, the random string will contain digits
    :return: The random string
    """

    chars = string.ascii_letters
    if contain_digits:
        chars += string.digits

    return "".join([random.choice(chars) for _ in range(length)])


def create_random_dir(base_name: str = "", time_: int = 10) -> str:
    """
    :param base_name: The base name of the dir, it will be added before the ID
    :param time_: The time (in minute) you want the file to exist (without touching it). Set it to 0 to make the file
    permanent since next reboot
    :return: The path of the temp dir
    """

    if base_name != "":
        base_name += "_"

    tmp = get_config("global.temp_dir")

    while True:
        id_ = __create_random_string()

        if not os.path.exists(f"{tmp}{os.sep}{time_}-{base_name}{id_}"):
            os.mkdir(f"{tmp}{os.sep}{time_}-{base_name}{id_}")
            logs.info("temp_manager", f"Created dir: {tmp}{os.sep}{time_}-{base_name}{id_}")
            return f"{tmp}{os.sep}{time_}-{base_name}{id_}"


def create_random_file(base_name: str = "", extension: str = "", time_: int = 10) -> str:
    """
    :param base_name: The base name of the file, it will be added before the ID
    :param extension: The extension of the file
    :param time_: The time (in minute) you want the file to exist (without touching it). Set it to 0 to make the file
    permanent since next reboot
    :return: The path of the temp file
    """

    if base_name != "":
        base_name += "_"

    if extension != "":
        if not extension.startswith("."):
            extension = f".{extension}"

    tmp = get_config("global.temp_dir")

    while True:
        id_ = __create_random_string()

        if not os.path.exists(f"{tmp}{os.sep}{time_}-{base_name}{id_}{extension}"):
            with open(f"{tmp}{os.sep}{time_}-{base_name}{id_}{extension}", "w"):
                pass
            logs.info("temp_manager", f"Created file: {tmp}{os.sep}{time_}-{base_name}{id_}{extension}")

            return f"{tmp}{os.sep}{time_}-{base_name}{id_}{extension}"


def purge_temp(all_: bool = False) -> None:
    """
    :param all_: A bool represent if you want all files to be deleted
    :return: None
    """

    dir_ = get_config("global.temp_dir")
    for i in os.listdir(dir_):
        try:
            if all_:
                if os.path.isfile(f"{dir_}{os.sep}{i}"):
                    os.remove(f"{dir_}{os.sep}{i}")
                else:
                    shutil.rmtree(f"{dir_}{os.sep}{i}")

            else:
                if int(i.split("-")[0]) != 0:
                    max_timestamp = time.time() - (int(i.split("-")[0])*60)

                    if os.stat(f"{dir_}{os.sep}{i}").st_mtime < max_timestamp:
                        logs.info("temp_manager", f"Removed: {dir_}{os.sep}{i}")
                        if os.path.isfile(f"{dir_}{os.sep}{i}"):
                            os.remove(f"{dir_}{os.sep}{i}")
                        else:
                            shutil.rmtree(f"{dir_}{os.sep}{i}")

        except Exception:
            pass
