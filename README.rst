PyMacro
=======

Features
--------

- Macro handler fully asynchronous
- Can create macros that loop while you press the button a 2nd time
- Can create hooks with multiple keys with "." (and) and "+" (or)
- Optimized for ram and CPU usage (nota: ensure you have a timeout with loop macros to avoid CPU usage)

Requirements
------------

- Python 3.8 or above
- For linux only: xdotool (can be installed with apt, pacman, dnf, ...)
- Does not work on MacOS

Installing
----------

You need to be in an empty folder with a shell with this directory in current working directory

.. code:: sh

    git clone https://github.com/picass02005/PyMacro.git  # If it doesn't work, download it from github directly

    #     Linux specific     #
    # ====================== #

    python3 -m pip install virtualenv
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    mkdir macros


    #    Windows specific    #
    # ====================== #

    python -m pip install virtualenv
    python -m venv venv
    venv\Scripts\activate.bat
    python -m pip install -r requirements.txt
    mkdir macros

Next, you need a script to launch it.

**Linux**

Use a service to run it at startup.

Nota 1: your working directory need to be the PyMacro's folder

Nota 2: On some environments, the process must run with another user than root (or the tray menu won't appear). If it's your case, specify in your service the user

If you want help, `RTFM <https://wiki.archlinux.org/title/Systemd>`_ (everything you need to know is here)

**Windows**
Create a file named **run_pymacro.bat** and copy paste the following:

.. code:: sh

    cd c:\path\to\your\PyMacro
    CALL venv\Scripts\activate.bat
    start pythonw run.py

Change the path in the cd to your PyMacro's folder

Put this script in **%AppData%\Microsoft\Windows\Start Menu\Programs\Startup**


Code your macros
----------------

If you run **create_macro_module.py**, it will create a module under **./macros/name** (name is asked by the script)

A module is composed by the following

::

    name
    ├── main.py
    ├── config.json
    └── modules

You can put every script you need to run the main.py under **./modules**

If you go in main.py, you'll see there is some imports:

.. code:: py

    from global_modules.get_config import get_config
    from global_modules.macro_manager import register
    from global_modules.macro_manager import disable_all_macros_for_window

Those are the main modules for users.

- **get_config**

    This add a function, **get_config()** which allow you to read json configs easily.

    .. code:: py

        temp_dir_folder = get_config("default.temp_dir")  # This will return the temp_dir field in the config.json at the root of the project
        example_config = get_config("test.config")  # This will return the config field in the config.json of the test module

    Run create_example_macros.py and read macros/example-2/main.py for an example in real case

- **register**

    This is a decorator used to register a macro. It has 3 parameters:

    - window: The window(s) where you want your macro to be working. If you set it to "default" it will work on any window if no window specific macro on same key(s) is defined
    - key: The key(s) you want to press to activate the macro. The "." can be used to mean "and" and the "+" can be used to mean "or". The or always take priority over the and. Example: "a.b+c" mean "(a and b) or c"
    - loop: Set it to True to make the macro looping until you press the key a 2nd time. Caution: put a asyncio.sleep of 0.1 seconds at the end of your macro to avoid an excessive cpu usage
    - before: An async function which will be called before the macro starts (useful with loop=True)
    - after: An async function which will be called before the macro end (useful with loop=True)

- **disable_all_macros_for_window**

    This function permit to disable all macros for a specific window (this include default ones)
    Usage: **disable_all_macros_for_window("window_name")**

Temp files
----------

You have temp_manager.py in global_modules to create temp files / temp folders.


Usage:

.. code:: py
    from global_modules import temp_manager

    temp_dir_path = temp_manager.create_random_dir(base_name="test", time_= 10)  # This will create a temp dir which name begin with "test" and which will last for 10 minutes after last edit in it
    temp_file_path = temp_manager.create_random_file(base_name="test", extension="txt", time_10)  # This will create a temp txt file which name begin with test and which last for 10 minutes after last edit

Example macros
--------------

To create example macros, you can run create_example_macros.py (it will create 2 example folders under **./macros**)

Support me
----------

You can support me on `my paypal <https://paypal.me/picasso2005>`_
