
class Player_location:
    out_of_bound_row = ((1, 0), (6, 2)) #(row, facing)
    out_of_bound_col = ((1, 3), (6, 1)) #(col, facing)
    def __init__(self, loc):
        if len(loc) != 3: raise Exception("Input location player tuple does not have length 3")
        (self.row, self.col, self.ep) = loc
        Player_location.check_valid(self)

    def __str__(self):
        return str(self.into_tuple())

    def into_tuple(self):
        return (self.row, self.col, self.ep)

    # checks wheter the location is out of bound/killed
    def out_of_bound(self):
        facing = self.ep // 2
        if (self.row, facing) in self.out_of_bound_row \
            or (self.col, facing) in self.out_of_bound_col:
            return True
        else:
            return False

    # check if the player's loc is valid
    def check_valid(player_loc):
        row, col, ep = player_loc.row, player_loc.col, player_loc.ep
        if (row,col) == (0, 0) or (row,col) == (0, 7) or (row,col) == (7, 7) or (row,col) == (7, 0):
            raise Exception("SPlayer loc set invalid, input is " + str(new_loc))
        if not 0 <= ep <= 7:
            raise Exception("endpoint invalid, endpoint" + str(ep))
        if not 0 <= row <= 7:
            raise Exception("row invalid, " + str(row))
        if not 0 <= col <= 7:
            raise Exception("col invalid, " + str(col))

        if row == 0 and not (ep == 4 or ep == 5) \
            or row == 7 and not (ep == 0 or ep == 1) \
            or col == 0 and not (ep == 2 or ep == 3) \
            or col == 7 and not (ep == 6 or ep == 7):
            raise Exception("player loc invalid, " + str((row, col, ep)))

    def check_pawn(player_loc):
        Player_location.check_valid(player_loc)
        row, col, ep = player_loc.into_tuple()
        facing = ep // 2

        if (row == 0 and facing == 2) \
           or (row == 7 and facing == 0) \
           or (col == 0 and facing == 1) \
           or (col == 7 and facing == 3):
           return True
        return False


class Tile_location:
    def __init__(self, loc):
        if len(loc) != 2: raise Exception("Input location player tuple does not have length 2")
        (self.row, self.col) = loc
        Tile_location.check_tile_loc(self)

    def __str__(self):
        return str(self.into_tuple())
        
    def into_tuple(self):
        return (self.row, self.col)

    def check_tile_loc(tile_loc):
        row, col = tile_loc.row, tile_loc.col
        if not (1 <= row <= 6 and 1 <= col <= 6):
            raise Exception("tile_loc not valid, tile_loc is " + str(tile_loc))
