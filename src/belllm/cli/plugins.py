from pathlib import Path
import subprocess
import belllm.plugins
from ..utils import get_root_dir


# TODO refresh enable disable
def parse_plugins(args):
    if len(args) < 1:
        print("CLI:")
        for cli_plugin in belllm.plugins.get_cli_plugins():
            print(" - ", cli_plugin)
        print("Initialisation:")
        for library in belllm.plugins.get_prechat_script():
            print(" - ", library['plugin'])
        print("Library:")
        for library in belllm.plugins.get_library():
            print(" - ", library)

        return

    command = args[0]
    if command == "help":
        print("`belllm plugins`: List belllm plugins")
        print("`belllm plugins help`: Shows this help message")
        print("`belllm plugins open`: Open the plugins dir")

    elif command == "open":
        plugins_dir = Path(get_root_dir() / "plugins")
        plugins_dir.mkdir(parents=True, exist_ok=True)

        subprocess.call(["open", "-R", str(plugins_dir)])

    else:
        print("Unknown command.")