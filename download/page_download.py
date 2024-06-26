import random

from modules.page import Page
from typing import Literal, TypeAlias
import aiohttp
import asyncio
Status: TypeAlias = Literal["IDLE", "DOWNLOADING", "FAILED", "FINISHED"]


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
            await asyncio.sleep(10)
            if random.choice([True, False]):
                self.switch_state_checked("FINISHED")
            else:
                self.switch_state_checked("FAILED")
            return True
        except Exception:
            self.switch_state_checked("FAILED")
            return False


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
