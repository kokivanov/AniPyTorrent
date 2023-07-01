from copy import copy, deepcopy
import datetime
from typing import List, Tuple
from typing import Callable
from client.file import File
from client.meta import Meta
from client.piece import Piece
from client.tracker import Tracker


class Torrent():
    @property
    def tracker_list(self):
        return self._trackerList

    @property
    def name(self):
        return self._name
    
    @property
    def created_by(self):
        return self._created_by
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def files(self):
        return self._pFiles

    @property
    def pieces(self):
        return self._pieces
    
    @property
    def actual_size(self):
        return self._actual_size
    
    def __len__(self):
        return self._actual_size
    
    @property
    def wirking_size(self):
        return self._working_zise



    # @property
    # def name(self):
    #     return self.info.

    def __init__(self, info: Meta, adder : Callable[[Meta], Tracker]):
        self._name : str = info.info.name
        self._created_by : str = info.created_by
        self._created_at : datetime = info.created
        self._trackerList : List[Tracker] = [adder(info)]
        self._pieces : List[Piece] = []
        self._files : List[File] = []
        self._piece_length = info.info.piece_length

        files_tmp = deepcopy(info.info.files)

        cur_piece_byte = 0
        end_piese_byte = cur_piece_byte + self._piece_length
        cur_file_byte = 0
        end_file_byte = cur_file_byte + files_tmp[0].length

        trans_file : Tuple[File, int] = None

        for piece_index, piece in enumerate(info.info.pieces):
            while cur_file_byte 



                    
        self._pFiles = [(i.path, i.length) for i in self._files]
        self._actual_size = sum(f.length for f in self._files)
        self._working_zise = len(self.pieces) * self._piece_length

        
