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

    def get_failed_times(self) -> int:
        ...

    def reset_failed_times(self):
        ...

    def get_max_failed_times(self) -> int:
        ...

    def set_max_failed_times(self, max_failed_times: int) -> None:
        ...
