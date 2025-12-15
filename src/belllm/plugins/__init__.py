import os

from belllm.utils import get_root_dir

# todo clean up the plugin api to make it feel more idomatic
# probably make a belllm.py file in each plugin whihch exposes everything but also make it run like a module
# todo also pass in a context when executing
# todo also allow for top level

_initialised = False
_preload_scripts = []
_library = {}
_cli = {}


def get_plugins_dir():
    return get_root_dir() / "plugins"


def get_library():
    if not _initialised:
        initialise_plugins()
    return _library


def get_cli_plugins():
    if not _initialised:
        initialise_plugins()
    return _cli


def get_prechat_script():
    if not _initialised:
        initialise_plugins()
    return _preload_scripts


def list_plugins():
    if get_plugins_dir().exists():
        return [x for x in os.listdir(get_plugins_dir()) if x[0] != "."]
    return []


def initialise_plugins():
    import sys
    import importlib

    _initialised = True
    _library.clear()
    _preload_scripts.clear()
    _cli.clear()

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
            if not function.endswith(".py"):
                continue

            spec = importlib.util.spec_from_file_location(plugin, get_plugins_dir() / plugin / function)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)


            for key, entry in foo.__dict__.items():
                if key.startswith("_"):
                    if key not in ["_initialise", "_cli"]:
                        continue

                if str(type(entry)) == "<class 'function'>":
                    plugin_name = plugin + "." + key

                    if key == "_initialise":
                        _preload_scripts.append({
                            "plugin": plugin,
                            "name": plugin_name,
                            "run": entry
                        })
                    elif key == "_cli":
                        _cli[plugin] = entry
                    else:
                        _library[plugin_name] = {
                            "plugin": plugin,
                            "function": entry,
                            "description": entry.__doc__,
                            "annotations": entry.__annotations__,
                        }


if __name__ == "__main__":
    initialise_plugins()
    breakpoint()
