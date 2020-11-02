from enum import Enum


class ItemType(Enum):
    SONG = 1
    ALBUM = 2


class OutputType(Enum):
    STD = 1
    CLIP = 2
    FILE = 3
    NONE = 4
