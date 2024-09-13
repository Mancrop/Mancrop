from plugins.plugins_manager import PluginsManager
from plugins.msource_def import MangaMetaData
import asyncio

if __name__ == "__main__":
    plugins_manager = PluginsManager("MangaCrawler")
    plugins_manager.load_plugins("src/plugins/bin/crawler/CrawlOmyschool.py")
    plugin = plugins_manager.get_plugin("木马漫画(omyschool)")
    plugins_manager.print_plugins()
    print("Author:", plugin.author())
    print("Description:", plugin.description())
    print("Version:", plugin.version())
    print("Name:", plugin.name())
    print("Type:", plugin.type())
    res = asyncio.run(plugin.search(MangaMetaData(name="我的青春恋爱物语果然有问题")))
    for i in res:
        print(i)
        