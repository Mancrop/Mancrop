import asyncio
from typing import Literal, TypeAlias
from typing import Protocol


Status: TypeAlias = Literal["IDLE", "DOWNLOADING", "FAILED", "FINISHED"]


class Downloader(Protocol):
    async def download(self) -> bool:
        ...

    async def get_progress(self) -> int:
        ...

    async def get_status(self) -> Status:
        ...

    def set_path(self, path: str) -> None:
        ...

    def get_path(self) -> str:
        ...


if __name__ == "__main__":
    from pathlib import Path
    import sys
    sys.path.insert(0, str((Path(__file__) / "../..").resolve()))
    from rich.progress import Progress, SpinnerColumn, BarColumn
    from download_queue import DownloadQueue
    from modules.page import Page
    from page_download import PageDownload

    progress = Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
    )

    async def main():
        cases = ["https://www.pwithe.com/Public/Upload/download/20170211/589ebf8e5bb13.pdf",
                 "https://www.baidu.com",
                 "https://blog.csdn.net/csdnnews/article/details/139859111?spm=1000.2115.3001.5928",
                 "https://www.cnblogs.com/zhiminyu/p/14202683.html",
                 "https://cloud.tencent.com/developer/article/1676325",
                 ]
        queue = []

        for idx, case in enumerate(cases):
            download_queue = DownloadQueue(f"../test/test{idx}", 10)
            pages_ = [PageDownload.from_page(Page(url=case), f"Page{i}", i) for i in range(50)]
            download_queue.add_items(pages_)
            queue.append(download_queue)

        top_downloader = DownloadQueue(f"../test", 10)
        top_downloader.add_items(queue)

        top_task = asyncio.create_task(top_downloader.download())

        tasks = []
        with progress:
            total = progress.add_task("[red]Total..")
            for idx, i in enumerate(queue):
                tasks.append((i, progress.add_task(f"[green]Chapter{idx}")))

            while not progress.finished:
                progress.update(total, completed=await top_downloader.get_progress())
                for queue, task in tasks:
                    progress.update(task, completed=await queue.get_progress())
                await asyncio.sleep(0.5)
        await asyncio.gather(top_task)

    asyncio.run(main())
