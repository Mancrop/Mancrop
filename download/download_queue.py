from page_download import PageDownload


class Queue:
    def __init__(self):
        self.queue: list[PageDownload] = []

    def add_page(self, page: PageDownload):
        self.queue.append(page)
