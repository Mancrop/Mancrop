import os
import asyncio
from download.page_download import PageDownload

if __name__ == "__main__":
    cur_path = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(cur_path, "../simple_try/test/")
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    async def test():
        task_list = []
        for i in range(10):
            page = PageDownload()
            page.url = "https://www.baidu.com"
            page.path = f"../test/baidu{i}.html"
            task_list.append(page.download())
        await asyncio.gather(*task_list)

    asyncio.run(test())