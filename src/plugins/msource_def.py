from modules.chapter import Chapter
from modules.page import Page
from .plugins_def import PluginsBase
from utils import string_normalize
from fuzzywuzzy import fuzz


"""
This file contains the definition of the MangaMetaData class and the MSource protocol.
Any of the manga source plugins should implement the MSource protocol.
MangaMetaData class is used to store the metadata of a manga. It contains the following attributes:
- name: The name of the manga.
- url: The URL of the manga.
- updated_date: The date when the manga was last updated.
- author: The author of the manga.
- description: The description of the manga.
- cover_img_url: The URL of the cover image of the manga.
Before seaching for a manga, the user can create a MangaMetaData object with the name of the manga and optionally other metadata. 
After seaching for a manga, the plugin should return a list of MangaDataAfterSearch objects, which contain the metadata of the manga and the URL of the manga.
The MSource protocol defines the methods that a manga source plugin should implement:
- search: This method takes a MangaMetaData object as input and returns a list of MangaDataAfterSearch objects.
- get_chapters: This method takes a MangaDataAfterSearch object as input and returns a list of Chapter objects.
- get_pages: This method takes a Chapter object as input and returns a list of Page objects.

MangaDataAfterSearch class is a subclass of MangaMetaData. It contains the following additional attributes:
- url: The URL of the manga.
- score: The score of the manga. The score is used to rank the search results.

So get_chapters should be used after search and get_pages should be used after get_chapters.

"""

class MangaMetaData:
    def __init__(self, name: str, updated_date: str | None = None, author: str | None = None, 
                 description: str | None = None, cover_img_url: str | None = None):
        self.name = name
        self.updated_date = updated_date
        self.author = author
        self.description = description
        self.cover_img_url = cover_img_url
        
    def __str__(self):
        return f"Name: {self.name}\n" \
        f"Updated date: {self.updated_date}\n"\
        f"Author: {self.author}\n"\
        f"Description: {self.description}\n"\
        f"Cover image URL: {self.cover_img_url}\n"
    
    def match_score(self, other: 'MangaMetaData') -> int:
        score = 0
        def match_score_helper(s1: str, s2: str, rate: int) -> int:
            normalized = string_normalize.string_normalize(s1)
            normalized_other = string_normalize.string_normalize(s2)
            fuzzywuzzy_score = fuzz.ratio(normalized, normalized_other)
            return fuzzywuzzy_score * rate
        
        score += match_score_helper(self.name, other.name, 10)
        if self.author is not None and other.author is not None:
            score += match_score_helper(self.author, other.author, 5)
        if self.updated_date is not None and other.updated_date is not None:
            score += match_score_helper(self.updated_date, other.updated_date, 3)
        if self.description is not None and other.description is not None:
            score += match_score_helper(self.description, other.description, 1)
        return score
    
    def set_cover_img_url(self, cover_img_url: str) -> None:
        self.cover_img_url = cover_img_url
        
class MangaDataAfterSearch(MangaMetaData):
    def __init__(self, manga_meta_data: MangaMetaData, url: str, score: int):
        super().__init__(manga_meta_data.name, manga_meta_data.updated_date, manga_meta_data.author, 
                         manga_meta_data.description, manga_meta_data.cover_img_url)
        self.url = url
        self.score = score
    
    def __str__(self):
        return f"Name: {self.name}\n" \
        f"Score: {self.score}\n" \
        f"URL: {self.url}\n" \
        f"Updated date: {self.updated_date}\n"\
        f"Author: {self.author}\n"\
        f"Description: {self.description}\n"\
        f"Cover image URL: {self.cover_img_url}\n"
        
    def get_url(self) -> str:
        return self.url
    
    def get_score(self) -> int:
        return self.score


class MSource(PluginsBase):
    async def search(self, query: MangaMetaData) -> list[MangaDataAfterSearch]:
        ...
        
    async def get_chapters(self, manga: MangaDataAfterSearch) -> list[Chapter]:
        ...
        
    async def get_pages(self, chapter: Chapter) -> list[Page]:
        ...
