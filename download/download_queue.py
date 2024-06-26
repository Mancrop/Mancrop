import asyncio
import os

from page_download import PageDownload
from modules.page import Page
from asyncio import Queue
from typing import Literal, TypeAlias

Status: TypeAlias = Literal["IDLE", "INFLIGHT", "FAILED", "FINISHED"]


class DownloadQueue:
    def __init__(self, path: str, max_reqs: int):
        self.pages: list[PageDownload] = []
        self.inflight_list: list[PageDownload] = []
        self.finished: int = 0
        self.status: Status = "IDLE"
        self.path: str = path
        self.max_reqs: int = max_reqs
        self.current_req_idx: int = 0

    def add_pages(self, pages: list[Page]):
        # Assume that pages is in order, ensure by caller
        for idx, page in enumerate(pages):
            path = os.path.join(self.path, "Page" + str(idx))
            self.pages.append(PageDownload.from_page(page, path, idx))

    async def producer(self, lock):
        while self.finished < len(self.pages):
            temp_list = []
            async with lock:
                for i in range(self.current_req_idx, self.current_req_idx + self.max_reqs):
                    if len(self.inflight_list) < self.max_reqs and i < len(self.pages):
                        page = self.pages[i]
                        self.inflight_list.append(page)
                        self.current_req_idx += 1
                        temp_list.append(page.download())
                    else:
                        break
            if temp_list:
                await asyncio.gather(*temp_list)
            await asyncio.sleep(0.1)  # 防止忙等待

    async def consumer(self, lock):
        while self.finished < len(self.pages):
            temp_list = []
            async with lock:
                for page in self.inflight_list[:]:
                    if page.status == "FINISHED":
                        self.inflight_list.remove(page)
                        self.finished += 1
                        print(self.finished)
                    elif page.status == "FAILED":
                        temp_list.append(page.download())

            if temp_list:
                await asyncio.gather(*temp_list)
            await asyncio.sleep(0.1)  # 防止忙等待

    async def start_download(self):
        lock = asyncio.Lock()
        producer_task = asyncio.create_task(self.producer(lock))
        consumer_task = asyncio.create_task(self.consumer(lock))
        await asyncio.gather(producer_task, consumer_task)


if __name__ == "__main__":
    download_queue = DownloadQueue("../test/", 10)
    page_ = Page(url="https://www.baidu.com")
    pages_ = [page_ for i in range(30)]
    download_queue.add_pages(pages_)
    asyncio.run(download_queue.start_download())
