from Tile import *
import random

class Deck():
    def __init__(self):
        self.num_tiles = 0
        self.tiles = []
        self.own_dragon = True

    def __str__(self):
        msg_num = "deck has " + str(self.num_tiles) + " tiles "
        msg_dragon = ""
        if self.own_dragon:
            msg_dragon = "with dragon\n"
        else:
            msg_dragon = "without dragon\n"

        msg_tiles = ""
        for t in self.tiles:
            msg_tiles += "\t" + str(t) + "\n"

        return msg_num + msg_dragon + msg_tiles

    def init(self):
        for (i, tile_path) in enumerate(Tile.legal_paths):
            self.add_tile(Tile(i, tile_path))
        self.shuffle()

    # public methods

    # accessors

    def get_num(self):
        return self.num_tiles

    def get_tiles(self):
        return self.tiles

    def is_empty(self):
        return self.num_tiles == 0

    def has_dragon(self):
        return self.own_dragon

    def __eq__(self,deck):
        if len(self.tiles) != len(deck.get_tiles()):
            return False
        # check both a in b and b in a
        for t in self.tiles:
            if t not in deck.get_tiles():
                return False
        for t in deck.get_tiles():
            if t not in self.tiles:
                return False
        return True

    # modifiers

    def shuffle(self):
        random.shuffle(self.tiles)

    def add_tile(self, tile):
        self.num_tiles += 1
        self.tiles.append(tile)

    def pop_tile(self):
        if self.num_tiles > 0:
            self.num_tiles -= 1
            return self.tiles.pop()
        elif self.own_dragon:
            self.own_dragon = False
            return None
        else:
            raise(Exception("Trying to draw card from deck when it is empty and has no dragon"))

    def return_dragon(self):
        if self.own_dragon == True:
            raise(Exception("Trying to return dragon when deck has dragon ???"))
        self.own_dragon = True
