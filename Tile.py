class Tile:
    legal_paths = (
    ((0, 1), (2, 3), (4, 5), (6, 7)), \
    ((0, 1), (2, 4), (3, 6), (5, 7)), \
    ((0, 6), (1, 5), (2, 4), (3, 7)), \
    ((0, 5), (1, 4), (2, 7), (3, 6)), \
    ((0, 2), (1, 4), (3, 7), (5, 6)), \
    ((0, 4), (1, 7), (2, 3), (5, 6)), \
    ((0, 1), (2, 6), (3, 7), (4, 5)), \
    ((0, 2), (1, 6), (3, 7), (4, 5)), \
    ((0, 4), (1, 5), (2, 6), (3, 7)), \
    ((0, 1), (2, 7), (3, 4), (5, 6)), \
    ((0, 2), (1, 7), (3, 4), (5, 6)), \
    ((0, 3), (1, 5), (2, 7), (4, 6)), \
    ((0, 4), (1, 3), (2, 7), (5, 6)), \
    ((0, 3), (1, 7), (2, 6), (4, 5)), \
    ((0, 1), (2, 5), (3, 6), (4, 7)), \
    ((0, 3), (1, 6), (2, 5), (4, 7)), \
    ((0, 1), (2, 7), (3, 5), (4, 6)), \
    ((0, 7), (1, 6), (2, 3), (4, 5)), \
    ((0, 7), (1, 2), (3, 4), (5, 6)), \
    ((0, 2), (1, 4), (3, 6), (5, 7)), \
    ((0, 7), (1, 3), (2, 5), (4, 6)), \
    ((0, 7), (1, 5), (2, 6), (3, 4)), \
    ((0, 4), (1, 5), (2, 7), (3, 6)), \
    ((0, 1), (2, 4), (3, 5), (6, 7)), \
    ((0, 2), (1, 7), (3, 5), (4, 6)), \
    ((0, 7), (1, 5), (2, 3), (4, 6)), \
    ((0, 4), (1, 3), (2, 6), (5, 7)), \
    ((0, 6), (1, 3), (2, 5), (4, 7)), \
    ((0, 1), (2, 7), (3, 6), (4, 5)), \
    ((0, 3), (1, 2), (4, 6), (5, 7)), \
    ((0, 3), (1, 5), (2, 6), (4, 7)), \
    ((0, 7), (1, 6), (2, 5), (3, 4)), \
    ((0, 2), (1, 3), (4, 6), (5, 7)), \
    ((0, 5), (1, 6), (2, 7), (3, 4)), \
    ((0, 5), (1, 3), (2, 6), (4, 7)))

    def __init__(self, index = -1, paths = (), rotation = 0):
        self.id = index           # non negative
        self.paths = paths         # 4 tuples of connected end points
        self.check_rotation(rotation)
        self.rotation = rotation     # [0, 3]
        self.sym_score = self.compute_sym_score()
        # TODO: add legal tile check in contructor
        # modify init_tile_2 as constructing a legal tile and the overwriting a invalid path

    def __str__(self):
        res = "Tile " + str(self.id) + ", rotation " + str(self.rotation) + " with path " + str(self.paths)
        return res
    # public methods

    # accessors
    def is_legal_tile(self):
        for p in self.legal_paths:
            if self.paths == p: return True
        return False

    def equal(self,t):
        if t.id == self.id and t.paths == self.paths:
            return True
        return False

    def __eq__(self, other):
        return self.equal(other)

    def get_rotation(self):
        return self.rotation

    def get_id(self):
        return self.id

    def get_sym_score(self):
        return self.sym_score

    def check_rotation(self,rotation):
        if rotation < 0 or rotation > 3:
            raise Exception("rotation is invalid, rotation = " + str(rotation))

    # modifiers

    def set_rotation(self, deg):
        if 0 <= deg <= 3:
            self.rotation = deg
        else:
            raise ValueError("set_rotation of tile input invalid, deg = "+ str(deg))

    def walk_path(self, entry):
        exit = -1
        for x,y in self.paths:
            if self.rotate(x) == entry:
                exit = self.rotate(y)
                break
            if self.rotate(y) == entry:
                exit = self.rotate(x)
                break
        if exit != -1: return exit
        raise Exception("No entry is matched when walking a tile, entry is " + str(entry))


    # private methods

    def rotate(self, ep):
        return self.compute_rotate(ep, self.rotation)

    def compute_rotate(self, ep, num):
        return (ep + num * 2) % 8

    def compute_sym_score(self):
        ways = []
        for i in range(4):
            cur = []
            for x,y in self.paths:
                a = self.compute_rotate(x, i)
                b = self.compute_rotate(y, i)
                if a < b:
                    cur.append([a,b])
                else:
                    cur.append([b,a])
                cur.sort(key = lambda x: x[0], reverse=True)
            if not cur in ways:
                ways.append(cur)
        return len(ways)
