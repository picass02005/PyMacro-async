import os

name = input("Type the name of the macro module you want to create\n>>> ")

os.mkdir(f"macros/{name}")
os.mkdir(f"macros/{name}/modules")

with open(f"macros/{name}/main.py", "w") as f:
    f.write(
        "from global_modules.get_config import get_config\n"
        "from global_modules.macros import register, disable_all_macros_for_window\n"
    )

with open(f"macros/{name}/config.json", "w") as f:
    f.write("{}")

print("Files created")
