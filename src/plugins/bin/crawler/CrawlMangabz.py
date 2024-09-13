from plugins.plugins_def import PluginsType
from plugins.msource_def import MSource, MangaMetaData, MangaDataAfterSearch
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from modules.chapter import Chapter
from modules.page import Page
from crawlee.playwright_crawler import PlaywrightCrawler


class CrawlMangabz(MSource):
    def __init__(self, *args, **kwargs) -> None:
        _ = args
        _ = kwargs
        self.search_results = []
        self.chapter_links = dict()
        
    def author(self) -> str:
        return "NamelessCoder"
    
    def description(self) -> str:
        return "从Mangabz(https://www.mangabz.com/)爬取漫画"
    
    def version(self) -> str:
        return "0.0.1"
    
    def name(self) -> str:
        return "Mangabz"
    
    def type(self) -> PluginsType:
        return "MangaCrawler"
    
    async def search(self, query: MangaMetaData) -> list[MangaDataAfterSearch]:
        search_crawler = PlaywrightCrawler()
        search_info = []
        
        @search_crawler.router.default_handler
        async def default_handler(context: PlaywrightCrawlingContext) -> None:
            context.log.info("default_handler")
            await context.page.wait_for_selector('input[id="txtKeywords"]')
            await context.page.fill('Input[id="txtKeyword"]', query.name)
            context.log.info(f"Search query: {query.name}")
            await context.page.click('a[id="btnSearch"]')
            context.log.info("Search button clicked")
            await context.page.wait_for_selector('div[class="result-list"] .comic-item')
            context.log.info(f"Current url: {context.request.url}")
            search_res = await context.page.query_selector_all('div[class="result-list"] .comic-item')
            for res in search_res:
                links = await res.query_selector('a')
                name = await links.get_attribute('title')
                url = await links.get_attribute('href')
                manga = MangaMetaData(name=name)
                match_score = query.match_score(manga)
                search_info.append(MangaDataAfterSearch(manga, url, match_score))
                
        await search_crawler.run(["https://www.mangabz.com/"])
        search_info.sort(key=lambda x: x.get_score(), reverse=True)
        return search_info


if __name__ == '__main__':
    import asyncio
    async def main():
        crawler = CrawlMangabz()
        search_results = await crawler.search(MangaMetaData(name="我的青春恋爱物语果然有问题"))
        for i in search_results:
            print(i)
    asyncio.run(main())
    