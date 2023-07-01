from typing import List
from client.meta import FileInfo
from client.piece import Piece

      

class File():

    @property
    def length(self):
        return self._lenght
    
    @property
    def md5sum(self):
        return self._md5sum
    
    @property
    def path(self):
        return self._path



    def __init__(self, info : FileInfo):
        self._lenght : str = info.length
        self._md5sum : str = info.md5sum
        self._path : str = info.path