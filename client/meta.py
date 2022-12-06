from collections import OrderedDict
from datetime import datetime
import hashlib

class fileInfo(object):
    """File info object for torrent"""
    def __init__(self, info : OrderedDict):
        try:
            self.path = [i.decode('utf8') for i in info[b'path']]
        except KeyError:
            try:
                self.path = info[b'name'].decode('utf-8')
            except KeyError:
                raise ValueError
        
        self.length = info[b'length']
        
        try:
            self.md5sum = info[b'md5sum'].hex()
        except KeyError:
            self.md5sum = None

    
class MetaInfo(object):
    def __init__(self, info: OrderedDict):
        """Base class for meta information

        Args:
            info (OrderedDict): info key of the .torrent metafile
            encoding (str): optional parameter encoding of the .torrent metafile ('UTF-8' by default).
        """

        self.name = info.get(b'name')
        self.piece_length = info.get(b'piece length')
        self.pieces = []

        for i in range(20, len(info[b'pieces']), 20):
            self.pieces.append(info[b'pieces'][i - 20: i].hex())

        self.type = None
        


class SingleFileMetaInfo(MetaInfo):
    """Factory class for creating metainfo object for single-file torrents.
    """

    def __init__(self, info: OrderedDict):
        """Factory class for creating metainfo object for single-file torrents.

        Args:
            info (OrderedDict): info key of the .torrent metafile
            encoding (str):  optional parameter encoding of the .torrent metafile ('UTF-8' by default).
        """
        self.file = fileInfo(info)
        self.type = 'S'
        super().__init__(info)
        

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

        for i in info[b'files']:
            self.files.append(fileInfo(i))
        
        self.type = 'M'
        super().__init__(info)


class MetaFactory(object):
    """Factory class for creating metainfo"""
    
    @staticmethod
    def _makeSingle(*args, **kwargs) -> SingleFileMetaInfo:
        return SingleFileMetaInfo(*args, **kwargs)

    @staticmethod
    def _makeMulti(*args, **kwargs) -> MultiFileMetainfo:
        return MultiFileMetainfo(*args, **kwargs)

    @staticmethod
    def makeMeta(info: OrderedDict) -> MetaInfo:
        """Depending on whether info dictionary has "files" attribute returns MultiFileMetainfo or SingleFileMetaInfo

        Args:
            info (OrderedDict): Parameter b'info' of Torrent file

        Returns:
            MetaInfo: MultiFileMetainfo or SingleFileMetaInfo
        """
        return MetaFactory._makeMulti(info) if b'files' in info.keys(
        ) else MetaFactory._makeSingle(info)


class Meta(object):
    """Class that contains required information for estabilishing data exchange."""
    
    def __init__(self, info: OrderedDict):
        """Class that contains required information for estabilishing data exchange.

        Args:
            info (OrderedDict): Torrent file metainfo
        """
        self.announce = info[b'announce'].decode('utf-8')
        try:
            self.announce_list = [
                [j.decode('utf-8') for j in i] for i in info[b'announce-list']]
        except KeyError:
            self.announce_list = None
        try:
            self.created = datetime.fromtimestamp(info[b'creation date'])
        except KeyError:
            self.created = None
        try:
            self.comment = info[b'comment'].decode('utf-8')
        except KeyError:
            self.comment = None
        try:
            self.created_by = info[b'created by'].decode('utf-8')
        except KeyError:
            self.created_by = None

        self.info = MetaFactory.makeMeta(info[b'info'])
