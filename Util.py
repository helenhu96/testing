from Tile import *
from MPlayer import *

def init_tile_1():
    return Tile(1, ((0,1),(2,3),(4,5),(6,7)), 0)

def init_tile_2(): # illegal tile
    return Tile(2, ((0,6),(2,4),(3,5),(1,7)), 0)

def init_tile_3():
    return Tile(3, ((0, 1), (2, 7), (3, 4), (5, 6)), 0)

def init_tile_4():
    return Tile(4, ((0, 7), (1, 5), (2, 3), (4, 6)), 0)

def init_tile_5():
    return Tile(5, ((0, 5), (1, 4), (2, 7), (3, 6)), 0)
    # +---*---*---+
    # |   |   |   |
    # *---+---+---*
    # |   |   |   |
    # *---+---+---*
    # |   |   |   |
    # +---*---*---+

def init_tile_6():
    return Tile(6, ((0, 4), (1, 5), (2, 7), (3, 6)), 0)

def init_tile_7():
    return Tile(7, ((0, 1), (2, 4), (3, 5), (6, 7)), 0)


def init_player_john():
    mplayer = MPlayer("John")
    mplayer.initialize("red", [])
    return mplayer

def init_player_mat():
    mplayer = MPlayer("Mat")
    mplayer.initialize("green", [])
    return mplayer







