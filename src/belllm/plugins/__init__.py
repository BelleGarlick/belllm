import os

from belllm.plugins.memory_bank import save_to_memory_bank
from belllm.utils import get_root_dir


library = None


def get_plugins_dir():
    return get_root_dir() / "plugins"


def list_plugins():
    return list(os.listdir(get_plugins_dir()))


def initialise_plugins():
    import sys
    import importlib

    global library

    library = {}

    library['memory_bank.save'] = {
        "function": save_to_memory_bank,
        "description": save_to_memory_bank.__doc__,
        "annotations": save_to_memory_bank.__annotations__,
    }

    for plugin in list_plugins():
    #     plugins[plugin] = {
    #         "functions": []
    #     }
    #
    #     if os.path.exists(get_plugins_dir() / plugin / "__init__.py"):
    #         # TODO import __init__
    #         spec = importlib.util.spec_from_file_location(plugin, get_plugins_dir() / plugin / "__init__.py")
    #         foo = importlib.util.module_from_spec(spec)
    #         spec.loader.exec_module(foo)
    #
    #         if "description" in foo.__dict__:
    #             plugins[plugin]["description"] = foo.description

        for function in os.listdir(get_plugins_dir() / plugin):
            if function == "__init__.py" or not function.endswith(".py"):
                continue

            spec = importlib.util.spec_from_file_location(plugin, get_plugins_dir() / plugin / function)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)

            if "run" in foo.__dict__:
                plugin_name = plugin + "." + function.replace(".py", "")
                library[plugin_name] = {
                    "function": foo.run,
                    "description": foo.run.__doc__,
                    "annotations": foo.run.__annotations__,
                }



if __name__ == "__main__":
    initialise_plugins()
    breakpoint()
