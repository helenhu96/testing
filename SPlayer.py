from Hand import *
from Location import *
from copy import deepcopy

class SPlayer:
    def __init__(self, index = -1, alive = True, loc = (1,1,1)):
        self.id = index # represent the color of the player
        self.alive = alive
        self.loc = Player_location(loc)  # (row, column, endpoint), (0, 0) is top left, endpoint (0..7)
        self.hand = Hand()
        self.player = None
        self.cheated = False

    # accessor
    def is_alive(self):
        return self.alive

    def possess_tile(self, tile):
        return self.hand.has_tile(tile)

    def get_id(self):
        return self.id

    def get_location(self):
        return self.loc

    def get_hand(self):
        return self.hand

    def get_hand_size(self):
        return self.hand.get_num()

    def is_hand_full(self):
        return self.hand.is_full()

    def is_hand_empty(self):
        return self.hand.is_empty()

    def get_cheated(self):
        return self.cheated

    def get_empty_spot(self):
        row, col, ep = self.get_location().into_tuple()
        facing = ep // 2

        # check if the starting Location is valid for first 4 conditions
        # check if on edge and facing outward for last 4 conditions
        if (row == 0 and facing != 2) \
            or (row == 7 and facing != 0) \
            or (col == 0 and facing != 1) \
            or (col == 7 and facing != 3) \
            or (row == 1 and facing == 0) \
            or (row == 6 and facing == 2) \
            or (col == 1 and facing == 3) \
            or (col == 6 and facing == 1):
            raise Exception("the player is facing toward the outside of board, \
                loc = " + str(self.get_location().into_tuple()))

        if facing == 0: return Tile_location((row - 1, col))
        if facing == 1: return Tile_location((row, col + 1))
        if facing == 2: return Tile_location((row + 1, col))
        if facing == 3: return Tile_location((row, col - 1))


    # modifiers
    def add_hand(self, tile):
        return self.hand.add_tile(tile)

    def sub_hand(self, tile):
        self.hand.sub_tile(tile)

    def return_hand(self, deck):
        self.hand.return_to_deck(deck)

    def draw_tile(self, deck):
        return self.add_hand(deck.pop_tile())

    def set_location(self, new_loc):
        self.loc = new_loc

    def set_cheated(self,cheated):
        self.cheated = cheated

    def set_alive(self,alive):
        self.alive = alive
