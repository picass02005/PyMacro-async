import json

from create_macro_module import create_macro_module

print("Creating some example macros...")

example1 = create_macro_module("classic_example")
with open(f"{example1}/main.py", "a") as f:
    f.write("\n\n"
            "@register(window=[\"default\"], key=\"a\", loop=False)\n"
            "async def a():\n"
            "    print(\"You pressed A\")\n\n\n"
            "@register(window=[\"discord\"], key=\"d.b+s\", loop=False)  # OR prioritize over AND\n"
            "async def discord():\n"
            "    print(\"You pressed (D and B) or S while being in discord\")\n\n\n"
            "disable_all_macros_for_window(\"explorer\")  # this will disable all macros when being in explorer\n")

example2 = create_macro_module("loop_config_example")
with open(f"{example2}/main.py", "a") as f:
    f.write("\nimport asyncio\n\n\n"
            "@register(window=[\"default\"], key=\"q\", loop=True)\n"
            "async def q():\n"
            "    print(\"You pressed Q and this macro will repeat until you press it another time\")\n"
            "    await asyncio.sleep(get_config(\"loop_config_example.timeout\"))  # will search for the value in loop_"
            "config_example/config.json\n")

with open(f"{example2}/config.json", "w") as f:
    f.write(json.dumps({'timeout': 0.5}, indent=4))

example3 = create_macro_module("before_after_example")
with open(f"{example3}/main.py", "a") as f:
    f.write("\nimport asyncio\n\n\n"
            "async def before_coro():\n"
            "    print(\"Before loop\")\n\n\n"
            "async def after_coro():\n"
            "    print(\"After loop\")\n\n\n"
            "@register(window=\"default\", key=\"v\", loop=True, before=before_coro, after=after_coro)\n"
            "async def v():\n"
            "    print(\"In loop\")\n"
            "    await asyncio.sleep(1)\n")

print("Created")
