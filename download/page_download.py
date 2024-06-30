import os.path
import shutil

from modules.page import Page
from download import Status
import aiohttp
import asyncio

"""
   The PageDownload class inherits from the Page class and implements page download functionality.

   Description:
       This class is used to manage and execute page download operations. It includes features such as managing download 
       status, setting the download path, and retrieving download progress.

   Attributes:
       status (Status): The current download status, initialized to "IDLE".
       path (str): The file save path for the download.
       failed_times (int): The current number of download failures, initialized to 0.
       max_failed_times (int): The maximum allowed number of download failures, initialized to 20.
"""


class PageDownload(Page):
    def __init__(self):
        super().__init__()
        self.status: Status = "IDLE"
        self.path: str = ""
        self.failed_times: int = 0
        self.max_failed_times: int = 20

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
        if self.failed_times >= self.max_failed_times:
            self.switch_state_checked("FAILED")
            return False
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1)) as session:
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
            self.failed_times += 1
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

    def get_failed_times(self) -> int:
        return self.failed_times

    def reset_failed_times(self):
        self.failed_times = 0

    def get_max_failed_times(self) -> int:
        return self.max_failed_times

    def set_max_failed_times(self, max_failed_times: int) -> None:
        self.max_failed_times = max_failed_times


if __name__ == "__main__":
    if not os.path.exists("../test/"):
        os.mkdir("../test/")

    async def test():
        task_list = []
        for i in range(10):
            page = PageDownload()
            page.url = "https://www.baidu.com"
            page.path = f"../test/baidu{i}.html"
            task_list.append(page.download())
        await asyncio.gather(*task_list)

    asyncio.run(test())
