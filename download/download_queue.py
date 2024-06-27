import asyncio
import os

from page_download import PageDownload
from modules.page import Page
from download import Status, Downloader


class DownloadQueue:
    def __init__(self, path: str, max_reqs: int):
        self.items: list[Downloader] = []
        self.inflight_list: list[Downloader] = []
        self.finished: int = 0
        self.status: Status = "IDLE"
        self.path: str = path
        self.max_reqs: int = max_reqs
        self.current_req_idx: int = 0
        self.lock = asyncio.Lock()

    def add_items(self, items: list[Downloader]):
        # Assume that pages is in order, ensure by caller
        # Don't care item idx here
        for idx, item in enumerate(items):
            path = os.path.join(self.path, item.get_path())
            item.set_path(path)
            self.items.append(item)

    async def producer(self):
        while self.finished < len(self.items):
            temp_list = []
            async with self.lock:
                for i in range(self.current_req_idx, self.current_req_idx + self.max_reqs):
                    if len(self.inflight_list) < self.max_reqs and i < len(self.items):
                        page = self.items[i]
                        self.inflight_list.append(page)
                        self.current_req_idx += 1
                        temp_list.append(page.download())
                    else:
                        break
            if temp_list:
                await asyncio.gather(*temp_list)
            await asyncio.sleep(0.1)  # Avoid busy waiting

    async def consumer(self):
        while self.finished < len(self.items):
            temp_list = []
            async with self.lock:
                for page in self.inflight_list[:]:
                    if await page.get_status() == "FINISHED":
                        self.inflight_list.remove(page)
                        self.finished += 1
                    elif await page.get_status() == "FAILED":
                        temp_list.append(page.download())

            if temp_list:
                await asyncio.gather(*temp_list)
            await asyncio.sleep(0.1)  # Avoid busy waiting

    async def download(self) -> bool:
        self.status = "DOWNLOADING"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        await asyncio.gather(self.producer(), self.consumer())
        self.status = "FINISHED"
        return True

    async def get_progress(self):
        async with self.lock:
            total = len(self.items)
            total_prog = sum([await item.get_progress() for item in self.items])/len(self.items) * 1.0
            progress = 100 if self.finished == total else int(total_prog)
            return progress

    async def get_status(self):
        async with self.lock:
            return self.status

    def set_path(self, path: str):
        self.path = path

    def get_path(self) -> str:
        return self.path


if __name__ == "__main__":
    download_queue = DownloadQueue("../test/queue1", 10)
    pages_ = [PageDownload.from_page(Page(url="https://www.baidu.com"), f"Page{i}", i) for i in range(30)]
    download_queue.add_items(pages_)
    asyncio.run(download_queue.download())
