"""
Type stubs for requests
"""

from typing import Any, Dict, Optional, Union, Mapping

class Response:
    def __init__(self) -> None: ...
    
    @property
    def status_code(self) -> int: ...
    
    @property
    def text(self) -> str: ...
    
    @property
    def headers(self) -> Dict[str, str]: ...
    
    def json(self) -> Any: ...

class Session:
    def __init__(self) -> None: ...
    
    def __enter__(self) -> 'Session': ...
    
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None: ...
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None, timeout: Optional[Union[int, float]] = None,
            allow_redirects: bool = True, **kwargs: Any) -> Response: ...
    
    def post(self, url: str, data: Optional[Any] = None, 
             headers: Optional[Dict[str, str]] = None, **kwargs: Any) -> Response: ...
    
    def put(self, url: str, data: Optional[Any] = None, 
            headers: Optional[Dict[str, str]] = None, **kwargs: Any) -> Response: ...
    
    def delete(self, url: str, **kwargs: Any) -> Response: ...
    
    @property
    def headers(self) -> Dict[str, str]: ...
    
    def update(self, headers: Dict[str, str]) -> None: ...
    
    def close(self) -> None: ...

def get(url: str, params: Optional[Dict[str, Any]] = None, 
        headers: Optional[Dict[str, str]] = None, timeout: Optional[Union[int, float]] = None,
        allow_redirects: bool = True, **kwargs: Any) -> Response: ...

def post(url: str, data: Optional[Any] = None, 
         headers: Optional[Dict[str, str]] = None, **kwargs: Any) -> Response: ...

def put(url: str, data: Optional[Any] = None, 
        headers: Optional[Dict[str, str]] = None, **kwargs: Any) -> Response: ...

def delete(url: str, **kwargs: Any) -> Response: ...

class RequestException(Exception):
    pass

class Timeout(RequestException):
    pass

class ConnectionError(RequestException):
    pass
