from typing import List
from client.file import File
from client.meta import PieceInfo

class FilePiece():

    @property
    def piece_end_byte(self):
        return self._piece_end_byte
    
    @property
    def piece_start_byte(self):
        return self._piece_start_byte
    
    @property
    def file(self):
        return self._file

    def __init__(self, file: File, piece_start_byte : int) -> None:
        self._piece_start_byte = piece_start_byte
        self._piece_end_byte = piece_start_byte + file.length
        self._file = file

class Piece():
    @property
    def number(self) -> int:
        return self._number

    @property
    def hash(self) -> int:
        return self._hash
    
    def __len__(self):
        return self._length
    
    @property
    def length(self):
        return self._length

    def __init__(self, number : int, info: PieceInfo, length : int, files : List[File], actual_length : int = None):
        self._number = number
        self._hash = info.hash
        self._working_length = length
        self._length = actual_length if actual_length else length
        self._files : List[FilePiece] = []
        cur_byte = 0
        for file in files:
            self._files.append(FilePiece(file, cur_byte))
            cur_byte += file.length