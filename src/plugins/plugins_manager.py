from .plugins_def import PluginsBase
import importlib.util


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
                return False
        except Exception as _:
            return True
        return False
    
    def remove_plugin(self, plugin_name: str) -> bool:
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            return True
        return False
        
    def get_plugin(self, plugin_name: str) -> PluginsBase | None:
        if plugin_name in self.plugins:
            return self.plugins[plugin_name]()
        return None