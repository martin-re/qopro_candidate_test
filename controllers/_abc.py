import importlib.util
from abc import abstractmethod

from aiohttp.web_request import Request
from aiohttp.web import Response


class Controller:
    """Base class for controllers.
    Is still possible to overwrite method and path properties if necesary."""

    @abstractmethod
    async def handler(self, request: Request) -> Response:
        return NotImplemented

    # FIXME: doesn't support multi-parameters in URI
    @property
    @abstractmethod
    def _parametrised(self) -> bool:
        """Should return True if endpoint contains parameter, otherwise False."""
        return NotImplemented
    
    @property
    def method(self) -> str:
        """Subclasses naming convention is via request method, 
        e.g: Get, Post, Delete, Put ..."""
        return self.__class__.__name__.upper()
    
    @property
    def path(self) -> str:
        """Structure is the dependency how to define endpoint path. (nesting directories).
        Last one must contain __init__.py where should be declared new Controller.
        E.g:
            http://<HOST>:<PORT>/price/history

            price
            └── history
                └── __init__.py """
        meta_path = importlib.util.find_spec(self.__class__.__module__).name.split('.')[1:]
        if self._parametrised:
            return '/' + ('/'.join(meta_path[: -1]) + '/' + '{' f'{meta_path[-1]}') + '}'
        else:
            return '/' + '/'.join(meta_path)
