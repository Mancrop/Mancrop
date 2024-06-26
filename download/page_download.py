from modules.page import Page
from typing import Literal, TypeAlias
import aiohttp
import asyncio
Status: TypeAlias = Literal["IDLE", "DOWNLOADING", "FAILED"]


class PageDownload(Page):
    def __init__(self):
        super().__init__()
        self.status: Status = "IDLE"
        self.path: str = ""
        self.index: int = 0

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

    async def download(self):
        self.switch_state_checked("DOWNLOADING")
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                response.raise_for_status()
                with open(f"{self.path}", "wb") as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        file.write(chunk)


if __name__ == "__main__":
    async def gather():
        task_list = []
        for i in range(10):
            page = PageDownload()
            page.url = "https://www.baidu.com"
            page.path = f"baidu{i}.html"
            task_list.append(page.download())
        return await asyncio.gather(*task_list)

    asyncio.run(gather())
