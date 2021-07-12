import os


def create_macro_module(name: str):
    if os.path.exists(f"macros/{name}"):
        raise FileExistsError("Module already exist")

    os.mkdir(f"macros/{name}")
    os.mkdir(f"macros/{name}/modules")

    with open(f"macros/{name}/main.py", "w") as f:
        f.write(
            "from global_modules.get_config import get_config\n"
            "from global_modules.macro_manager import disable_all_macros_for_window\n"
            "from global_modules.macro_manager import register\n"
        )

    with open(f"macros/{name}/config.json", "w") as f:
        f.write("{}")

    return f"macros/{name}"


if __name__ == "__main__":
    create_macro_module(input("Type the name of the macro module you want to create\n>>> "))
    print("Files created")
