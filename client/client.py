from collections import OrderedDict
import datetime
import hashlib
from client.torrent import Torrent

from client.utils.bencoder import Decoder

from .info import VERSION
from .tracker import Tracker
from .meta import Meta


class Client(object):
    """
        Class that represents your BitTorrent client. That class contains all essential methods to interact with your files. 
    """

    def __init__(self, peer_id=hashlib.md5(str(datetime.datetime.now().timestamp()).encode()).hexdigest()[:12]) -> None:
        """
        Client constructor.

        peer_id is optional argument, it will be generated from current timestamp. 
        """

        if len(peer_id) > 12:
            raise ValueError("Id can't be longer than 12")

        self.peer_id = ascii(f'-AN{VERSION}-' + peer_id)
        self.trackers: dict[str, Tracker] = {}
        self.torrentsQ: dict[str, Torrent] = dict()

    def _add_tracker(self, metafile: Meta) -> Tracker:
        if not metafile.announce in self.trackers.keys():
            self.trackers[metafile.announce] = Tracker(metafile, self.peer_id)
            return self.trackers[metafile.announce]
        else:
            return self.trackers[metafile.announce]

    def _add_from_meta(self, metafile: Meta):
        self.torrentsQ[metafile.info.name] = Torrent(metafile, self._add_tracker)

    def add_from_dict(self, metafile: OrderedDict | dict):
        """
            Add Torrent to queue from dictionary that represents decoded file or magnet link
        """
        tmp = Meta(metafile)
        self._add_from_meta(tmp)

    def add_from_file(self, path: str):
        """
            Add Torrent to queue from provided .torrent file
        """
        try:
            a: Decoder = None
            with open(path, 'rb') as f:
                a = Decoder(f.read())
            self.add_from_dict(a.decode())
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise e
