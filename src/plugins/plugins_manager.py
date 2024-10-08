from .plugins_def import PluginsBase
import importlib.util

"""
Plugins mangaer is a class that manages plugins
It can load plugins from a file, and store them in a dictionary
Methods are list below:
- __init__: init plugins manager
- load_plugins: load plugins from file, noting that the name of plugins class 
should the same as the file
- print_plugins: ...
- ...

There is a using example for this class, see test_plugins_manager.py
"""

class PluginsManager():
    def __init__(self, plugins_type: str):
        self.plugins: dict[str, PluginsBase] = {}
        self.plugins_type = plugins_type
        
    def load_plugins(self, plugin_path: str, *args, **kwargs) -> bool:
        # plugin is a python file
        # plugin's main class should inherit from PluginsBase, and named as the file name
        module_name = plugin_path.split("/")[-1].split(".")[0]
        main_class_name = module_name
        try:
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            main_class = getattr(module, main_class_name)
            if main_class().type() == self.plugins_type:
                class_obj = main_class(args, kwargs)
                self.plugins[class_obj.name()] = class_obj
                return True
        except Exception as e:
            print(f'Load plugin {plugin_path} failed: {e}')
            return False
        return False
    
    def print_plugins(self) -> None:
        print("Plugins:")
        for plugin in self.plugins:
            print(plugin)
        print()
    
    def remove_plugin(self, plugin_name: str) -> bool:
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            return True
        return False
        
    def get_plugin(self, plugin_name: str) -> PluginsBase | None:
        if plugin_name in self.plugins:
            return self.plugins[plugin_name]
        return None