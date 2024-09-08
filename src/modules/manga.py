from typing import Literal


class Manga:
    def __init__(self, url: str = ""):
        self.url = url
        self.title = ""
        self.artist: str | None = None
        self.author: str | None = None
        self.description: str | None = None
        self.genre: str | None = None
        self.status: Literal["ALWAYS_UPDATE", "ONLY_FETCH_ONCE"]
        self.thumbnail_url: str | None = None
        # update strategy ...
        self.initialized: bool = False
