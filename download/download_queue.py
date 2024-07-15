import asyncio
import os

from page_download import PageDownload
from modules.page import Page
from download import Status, Downloader

"""
The DownloadQueue class is responsible for managing the download process of a list of Downloader objects. It provides the following functionality:

1. Adds items (Downloader objects) to the queue.
2. Manages the download process using producer and consumer tasks, ensuring that the maximum number of concurrent requests is not exceeded.
3. Handles failed downloads by retrying them up to a specified maximum number of times.
4. Keeps track of the overall download progress and status.
5. Allows setting the download path and maximum number of failed attempts.

The class uses a lock to ensure thread-safe access to shared resources, such as the lists of items, in-flight requests, and failed requests.
"""


class DownloadQueue:
    def __init__(self, path: str, max_reqs: int):
        self.items: list[Downloader] = []
        self.inflight_list: list[Downloader] = []
        self.failed_list: list[Downloader] = []
        self.finished: int = 0
        self.status: Status = "IDLE"
        self.path: str = path
        self.max_reqs: int = max_reqs
        self.current_req_idx: int = 0
        self.lock = asyncio.Lock()
        self.max_failed_times: int = 3
        self.failed_times = 0

    def add_items(self, items: list[Downloader]):
        # Assume that pages is in order, ensure by caller
        # Don't care item idx here
        for idx, item in enumerate(items):
            path = os.path.join(self.path, item.get_path())
            item.set_path(path)
            self.items.append(item)

    async def producer(self):
        while self.finished < len(self.items) and self.status == "DOWNLOADING":
            if self.failed_times >= self.max_failed_times:
                self.status = "FAILED"
                return
            temp_list = []
            async with self.lock:
                if self.failed_list:
                    failed_temp = [item.download() for item in self.failed_list]
                    temp_list.extend(failed_temp)
                    self.failed_list.clear()
                assert len(self.inflight_list) <= self.max_reqs
                for i in range(self.current_req_idx, self.current_req_idx + self.max_reqs):
                    if len(self.inflight_list) < self.max_reqs and i < len(self.items):
                        page = self.items[i]
                        self.inflight_list.append(page)
                        self.current_req_idx += 1
                        temp_list.append(page.download())
                    else:
                        break
                not_max_failed = False
                for item in self.inflight_list:
                    if item.get_failed_times() < self.max_failed_times:
                        not_max_failed = True
                        break
                if not not_max_failed:
                    self.failed_times += 1
            if temp_list:
                await asyncio.gather(*temp_list)
            await asyncio.sleep(0.1)  # Avoid busy waiting
        if self.status == "DOWNLOADING":
            self.status = "FINISHED"

    async def consumer(self):
        while self.finished < len(self.items) and self.status == "DOWNLOADING":
            async with self.lock:
                for page in self.inflight_list[:]:
                    if await page.get_status() == "FINISHED":
                        self.inflight_list.remove(page)
                        self.finished += 1
                    elif await page.get_status() == "FAILED":
                        if page.get_failed_times() < page.get_max_failed_times():
                            self.failed_list.append(page)

            await asyncio.sleep(0.1)  # Avoid busy waiting

    async def download(self) -> bool:
        self.status = "DOWNLOADING"
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        await asyncio.gather(self.producer(), self.consumer())
        if self.status == "FINISHED":
            return True
        else:
            return False

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

    def get_failed_times(self) -> int:
        return self.failed_times

    def reset_failed_times(self):
        for i in self.items:
            i.reset_failed_times()
        self.failed_times = 0

    def get_max_failed_times(self) -> int:
        return self.max_failed_times

    def set_max_failed_times(self, max_failed_times: int) -> None:
        self.max_failed_times = max_failed_times


if __name__ == "__main__":
    cur_path = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(cur_path, "../simple_try/test/")
    download_queue = DownloadQueue(os.path.join(target_path, "queue1"), 10)
    pages_ = [PageDownload.from_page(Page(url="https://www.baidu.com"), f"Page{i}", i) for i in range(30)]
    download_queue.add_items(pages_)
    asyncio.run(download_queue.download())
