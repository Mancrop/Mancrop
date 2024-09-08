
class Page:
    def __init__(self, index: int = 0, url: str = ""):
        self.index = index
        self.url = url
        self.imageUrl: str | None = None
