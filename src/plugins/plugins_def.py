from typing import Protocol
from typing import Literal, TypeAlias

PluginsType: TypeAlias = Literal["MangaCrawler"]


class PluginsBase(Protocol):
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def author(self) -> str:
        ...
    
    def description(self) -> str:
        ...
        
    def version(self) -> str:
        ...
    
    def name(self) -> str:
        ...
    
    def type(self) -> PluginsType:
        # type must be stable, so that the plugins manager can identify the plugin type
        ...
