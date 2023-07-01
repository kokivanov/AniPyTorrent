from typing import Mapping
from aiohttp import request


class Tracker(object):
    async def _make_request(self, par : Mapping[str, str] | None):
        return await request("GET", self.tackerURL, params=par)
        
    async def make_handhsake(s):
        s._make_request()
    
    def __init__(self, URL : str, peer_id : str):
        self.tackerURL = URL
        self._peer_id = peer_id

    @property
    def url(self) -> str:
        return self.tackerURL
    
    @property
    def peer_id(self) -> str:
        return self._peer_id

    
