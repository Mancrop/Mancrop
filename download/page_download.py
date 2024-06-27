from modules.page import Page
from download import Status
import aiohttp
import asyncio


class PageDownload(Page):
    def __init__(self):
        super().__init__()
        self.status: Status = "IDLE"
        self.path: str = ""

    @staticmethod
    def from_page(page: Page, path: str, index: int) -> "PageDownload":
        page_download = PageDownload()
        page_download.index = index
        page_download.url = page.url
        page_download.imageUrl = page.imageUrl
        page_download.path = path
        return page_download

    def switch_state_checked(self, status: Status) -> bool:
        if self.status == "IDLE" and status == "DOWNLOADING":
            self.status = status
            return True
        elif self.status == "DOWNLOADING" and status != "IDLE":
            self.status = status
            return True
        elif self.status == "FAILED" and status == "DOWNLOADING":
            self.status = status
            return True

        return False

    async def download(self) -> bool:
        self.switch_state_checked("DOWNLOADING")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    with open(f"{self.path}", "wb") as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
            self.switch_state_checked("FINISHED")
            return True
        except Exception:
            self.switch_state_checked("FAILED")
            return False

    async def get_progress(self) -> int:
        if self.status == "FINISHED":
            return 100
        else:
            return 0

    async def get_status(self) -> Status:
        return self.status

    def set_path(self, path: str) -> None:
        self.path = path

    def get_path(self) -> str:
        return self.path

if __name__ == "__main__":
    async def test():
        task_list = []
        for i in range(10):
            page = PageDownload()
            page.url = "https://www.baidu.com"
            page.path = f"../test/baidu{i}.html"
            task_list.append(page.download())
        await asyncio.gather(*task_list)

    asyncio.run(test())
