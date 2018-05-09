from Tile import *
from Deck import *
from copy import deepcopy

class Hand:
    def __init__(self):
        self.num_tiles = 0
        self.tiles = []

    # public methods

    # accessor
    def get_num(self):
        return self.num_tiles

    def get_tiles(self):
        return self.tiles

    def has_tile(self,tile):
        for t in self.tiles:
            if tile.equal(t):
                return True
        return False

    def is_full(self):
        return self.num_tiles == 3

    def is_empty(self):
        return self.num_tiles == 0

    # modifier

    # return true: added dragon tile
    # return false: added a non-dragon tile
    def add_tile(self, tile):
        if not tile: # handle dragon card
            return True
        elif tile.is_legal_tile():
            self.num_tiles += 1
            self.tiles.append(tile)
            return False
        else:
            raise(Exception("Trying to add illegal tile to hand, " + str(tile)))


    def sub_tile(self,tile):
        if self.has_tile(tile):
            self.num_tiles -= 1
            self.tiles.remove(tile)
        else:
            raise Exception("Trying to remove a tile not in hand, tile is " + str(tile))

    def return_to_deck(self, deck):
        for tile in self.tiles:
            deck.add_tile(tile)
        self.num_tiles = 0
        self.tiles = []

    # return all tile/orientation combinations, excluding the passed in tile_orientation pair
    def enumerate_tiles(self, tile):
        enum = []
        for t in self.tiles:
            for i in range(4):
                if t.equal(tile):
                    if i != tile.get_rotation():
                        new_tile = deepcopy(t)
                        new_tile.set_rotation(i)
                        enum.append(new_tile)
                else:
                    new_tile = deepcopy(t)
                    new_tile.set_rotation(i)
                    enum.append(new_tile)
        return enum
