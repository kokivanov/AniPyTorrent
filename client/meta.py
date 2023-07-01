from collections import OrderedDict
from datetime import datetime
import hashlib
from typing import Union, List

from client.exceptions import CorruptedFileExeption

class FileInfo(object):
    """File info object for torrent"""
    def __init__(self, info : OrderedDict):
        try:
            self.path : str = "/".join([i.decode('utf8') for i in info[b'path']])
        except KeyError:
            try:
                self.path : str = info[b'name'].decode('utf-8')
            except KeyError:
                raise CorruptedFileExeption(f"Can't find path or name in provided config")
        
        self.length : int = int(info[b'length'])
        
        try:
            self.md5sum : str = bytes(info[b'md5sum']).hex()
        except KeyError:
            self.md5sum : str = None

    
class MetaInfo(object):
    def __init__(self, info: OrderedDict[bytes, bytes]):
        """Base class for meta information

        Args:
            info (OrderedDict): info key of the .torrent metafile
            encoding (str): optional parameter encoding of the .torrent metafile ('UTF-8' by default).
        """

        self.files : List[FileInfo]
        
        self.name : str = info.get(b'name').decode()
        self.piece_length : int = info.get(b'piece length')
        self.pieces : List[PieceInfo] = []

        for i in range(20, len(info[b'pieces'])+1, 20):
            self.pieces.append(PieceInfo(info[b'pieces'][i - 20: i]))

        self.multifile = None
        


class SingleFileMetaInfo(MetaInfo):
    """Factory class for creating metainfo object for single-file torrents.
    """

    def __init__(self, info: OrderedDict):
        """Factory class for creating metainfo object for single-file torrents.

        Args:
            info (OrderedDict): info key of the .torrent metafile
            encoding (str):  optional parameter encoding of the .torrent metafile ('UTF-8' by default).
        """
        self.pieces : List[PieceInfo]
        self.files = [FileInfo(info)]
        super().__init__(info)
        self.multifile = False
        

class MultiFileMetainfo(MetaInfo):
    """Factory class for creating metainfo object for multi-files torrents.
    """

    def __init__(self, info: OrderedDict):
        """Factory class for creating metainfo object for multi-files torrents.

        Args:
            info (OrderedDict): info key of the .torrent metafile
            encoding (str): optional parameter encoding of the .torrent metafile ('UTF-8' by default).
        """
        self.files = []
        self.pieces : List[PieceInfo]
        for i in info[b'files']:
            self.files.append(FileInfo(i))
        
        super().__init__(info)
        self.multifile = True


class MetaFactory(object):
    """Factory class for creating metainfo"""
    
    @staticmethod
    def _makeSingle(*args, **kwargs) -> SingleFileMetaInfo:
        return SingleFileMetaInfo(*args, **kwargs)

    @staticmethod
    def _makeMulti(*args, **kwargs) -> MultiFileMetainfo:
        return MultiFileMetainfo(*args, **kwargs)

    @staticmethod
    def makeMeta(info: OrderedDict) -> MultiFileMetainfo | SingleFileMetaInfo:
        """Depending on whether info dictionary has "files" attribute returns MultiFileMetainfo or SingleFileMetaInfo

        Args:
            info (OrderedDict): Parameter b'info' of Torrent file

        Returns:
            MetaInfo: MultiFileMetainfo or SingleFileMetaInfo
        """
        return MetaFactory._makeMulti(info) if b'files' in info.keys(
        ) else MetaFactory._makeSingle(info)


class PieceInfo():
    def __init__(self, piece : bytes):
        self.value = piece
    
    @property
    def hash(self):
        return self.value.hex()

class Meta(object):
    """Class that contains required information for estabilishing data exchange."""
    
    def __init__(self, info: OrderedDict):
        """Class that contains required information for estabilishing data exchange.

        Args:
            info (OrderedDict): Torrent file metainfo
        """
        self.announce = (info.get(b'announce') or b'').decode('utf-8')
        self.announce_list = [
                [j.decode('utf-8') for j in i] for i in info.get(b'announce-list') or []
        ]
        self.created = datetime.fromtimestamp((info.get(b'creation date') or datetime.now().timestamp()))
        self.comment = (info.get(b'comment') or b'').decode('utf-8')
        self.created_by = (info.get(b'created by') or b'').decode('utf-8')        
        self.info : SingleFileMetaInfo | MultiFileMetainfo = MetaFactory.makeMeta(info[b'info'])


