from plugins.plugins_def import PluginsType
from plugins.msource_def import MSource, MangaMetaData, MangaDataAfterSearch
from crawlee.playwright_crawler import PlaywrightCrawlingContext
from modules.chapter import Chapter
from modules.page import Page
from crawlee.playwright_crawler import PlaywrightCrawler


class CrawlOmyschool(MSource):
    def __init__(self, *args, **kwargs) -> None:
        _ = args
        _ = kwargs
        self.search_results = []
        self.chapter_links = dict()
        
    def author(self) -> str:
        return "NamelessCoder"
    
    def description(self) -> str:
        return "从木马漫画(https://omyschool.com/)爬取漫画"
    
    def version(self) -> str:
        return "0.0.1"
    
    def name(self) -> str:
        return "木马漫画(omyschool)"
    
    def type(self) -> PluginsType:
        return "MangaCrawler"
    
    async def search(self, query: MangaMetaData) -> list[MangaDataAfterSearch]:
        search_crawler = PlaywrightCrawler()
        search_info = []
        
        @search_crawler.router.default_handler
        async def default_handler(context: PlaywrightCrawlingContext) -> None:
            context.log.info("default_handler")
            await context.page.wait_for_selector('input[id="input_search"]')
            await context.page.fill('Input[id="input_search"]', query.name)
            context.log.info(f"Search query: {query.name}")
            await context.page.click('button[id="searchsubmit"]')
            context.log.info("Search button clicked")
            await context.page.wait_for_selector('div[id="book_list"] .item')
            context.log.info(f"Current url: {context.request.url}")
            search_res = await context.page.query_selector_all('div[id="book_list"] .item')
            for res in search_res:
                links = await res.query_selector('a[title]')
                name = await links.get_attribute('title')
                url = await links.get_attribute('href')
                url = f"https://omyschool.com{url}"
                manga = MangaMetaData(name=name)
                match_score = query.match_score(manga)
                search_info.append(MangaDataAfterSearch(manga, url, match_score))
                
        await search_crawler.run(["https://omyschool.com/"])
        search_info.sort(key=lambda x: x.get_score(), reverse=True)
        return search_info
    
    async def get_chapters(self, manga: MangaDataAfterSearch) -> list[Chapter]:
        pass
    
    async def get_pages(self, chapter: Chapter) -> list[Page]:
        pass              
            
if __name__ == "__main__":
    import asyncio
    async def main() -> None:
        crawler = CrawlOmyschool()
        search_res = await crawler.search(MangaMetaData(name="我的青春恋爱物语果然有问题"))
        for i in search_res:
            print(i)
        
    asyncio.run(main())
    