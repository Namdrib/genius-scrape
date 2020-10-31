from enum import Enum
class ItemType(Enum):
    SONG = 1
    ALBUM = 2

#     # methods for argparse
#     def __str__(self):
#         return self.name.lower()
# 
#     def __repr__(self):
#         return str(self)
# 
#     @staticmethod
#     def argparse(s):
#         try:
#             return ItemType[s.upper()]
#         except KeyError:
#             return s


class OutputType(Enum):
    STD = 1
    CLIP = 2
    FILE = 3
    NONE = 4

#     # methods for argparse
#     def __str__(self):
#         return self.name.lower()
# 
#     def __repr__(self):
#         return str(self)
# 
#     @staticmethod
#     def argparse(s):
#         try:
#             return OutputType[s.upper()]
#         except KeyError:
#             return s

