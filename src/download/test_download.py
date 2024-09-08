import asyncio

if __name__ == "__main__":
    from rich.progress import Progress, SpinnerColumn, BarColumn
    from download_queue import DownloadQueue
    from modules.page import Page
    from page_download import PageDownload
    import os

    progress = Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
    )

    async def main():
        cases = ["https://tieba.baidu.com/f?kw=%E6%98%8E%E6%97%A5%E6%96%B9%E8%88%9F%E5%86%85%E9%AC%BC",
                 "https://www.baidu.com",
                 "https://tieba.baidu.com/f?kw=%E7%BB%88%E6%9C%AB%E5%9C%B0",
                 "https://www.cnblogs.com/zhiminyu/p/14202683.html",
                 "https://cloud.tencent.com/developer/article/1676325",
                 ]
        queue = []

        cur_path = os.path.dirname(os.path.abspath(__file__))
        print(cur_path)

        for idx, case in enumerate(cases):
            download_queue = DownloadQueue(os.path.join(cur_path, f"../simple_try/test/test{idx}"), 10)
            pages_ = [PageDownload.from_page(Page(url=case), f"Page{i}", i) for i in range(50)]
            download_queue.add_items(pages_)
            queue.append(download_queue)

        top_downloader = DownloadQueue(os.path.join(cur_path, f"../simple_try/test"), 10)
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
