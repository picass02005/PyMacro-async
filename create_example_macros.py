import json

from create_macro_module import create_macro_module

print("Creating some example macros...")

example1 = create_macro_module("example_1")
with open(f"{example1}/main.py", "a") as f:
    f.write("\n\n"
            "@register(window=[\"default\"], key=\"a\", loop=False)\n"
            "async def a():\n"
            "    print(\"You pressed A\")\n\n\n"
            "@register(window=[\"discord\"], key=\"d+b.s\", loop=False)  # OR prioritize over AND\n"
            "async def discord():\n"
            "    print(\"You pressed (D and B) or S while being in discord\")\n\n\n"
            "disable_all_macros_for_window(\"explorer\")  # this will disable all macros when being in explorer\n")

example2 = create_macro_module("example_2")
with open(f"{example2}/main.py", "a") as f:
    f.write("\nimport asyncio\n\n\n"
            "@register(window=[\"default\"], key=\"q\", loop=True)\n"
            "async def q():\n"
            "    print(\"You pressed Q and this macro will repeat until you press it another time\")\n"
            "    await asyncio.sleep(get_config(\"example_2.timeout\"))  # will search for the value in example_2/confi"
            "g.json\n")

with open(f"{example2}/config.json", "w") as f:
    f.write(json.dumps({'timeout': 0.5}, indent=4))

print("Created")
