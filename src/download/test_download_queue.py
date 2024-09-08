import asyncio
import os
from download.download_queue import DownloadQueue
from download.page_download import PageDownload
from modules.page import Page

if __name__ == "__main__":
    cur_path = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(cur_path, "../simple_try/test/")
    download_queue = DownloadQueue(os.path.join(target_path, "queue1"), 10)
    pages_ = [PageDownload.from_page(Page(url="https://www.baidu.com"), f"Page{i}", i) for i in range(30)]
    download_queue.add_items(pages_)
    asyncio.run(download_queue.download())
