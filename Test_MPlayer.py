import unittest

import Server
from Player import *
from MPlayer import *
from Util import *
from Location import *


class Test_MPlayer(unittest.TestCase):

    def reset_player_color(self):
        Player.available_colors = ["blue", "red", "green", "orange", "sienna", "hotpink", "darkgreen", "purple"]

    def setup(self):
        server = Server.Server.reset_get_instance()
        self.reset_player_color()
        mplayer_1 = init_player_john()
        mplayer_1.color = "red"
        hand = Hand()
        board = Board()
        server.board = board
        loc = (2,2,2)
        mplayer_1.place_pawn(board)
        mplayer_1.loc = Player_location(loc)
        splayer = SPlayer("red", True, loc)
        splayer.hand = hand
        splayer.player = mplayer_1
        server.splayers_active.append(splayer)
        tile_3 = init_tile_3() # sym 4
        tile_5 = init_tile_5() # sym 1
        tile_6 = init_tile_6() # sym 2
        hand.add_tile(tile_3)
        hand.add_tile(tile_5)
        hand.add_tile(tile_6)
        tiles = [tile_3, tile_5, tile_6]
        return mplayer_1, board, hand, tiles

    def test_get_name(self):
        self.reset_player_color()
        mplayer_1 = init_player_john()
        self.assertEqual(mplayer_1.get_name(), "John")

    def test_initialize(self):
        self.reset_player_color()
        mplayer_1 = init_player_john()
        self.assertEqual(mplayer_1.color, "red")
        self.assertEqual(mplayer_1.all_players_color, [])

        with self.assertRaises(Exception):
            mplayer_1.initialize("red", [])


        with self.assertRaises(Exception):
            mplayer_1.initialize(valid_color, all_colors)

        mplayer_2 = init_player_mat()
        with self.assertRaises(Exception):
            mplayer_1.initialize(invalid_color, all_colors)

    def test_place_pawn(self):
        for i in range(100):
            self.reset_player_color()
            mplayer_1 = init_player_john()
            board = Board()
            loc = mplayer_1.place_pawn(board)
            Player_location.check_valid(loc)


    def test_random_play(self):
        self.reset_player_color()
        mplayer_1, board, hand, tiles = self.setup()
        mplayer_1.set_strategy(Strategy.RANDOM)

        tile = mplayer_1.play_turn(board, hand, 15)
        self.assertTrue(tile in tiles)


    def test_symmetric_play(self):
        self.reset_player_color()
        mplayer_1, board, hand, tiles = self.setup()
        mplayer_1.set_strategy(Strategy.MOST_SYM)

        tile = mplayer_1.play_turn(board, hand, 15)
        tiles.sort(key = lambda x: x.get_sym_score())
        self.assertTrue(tile.equal(tiles[0]))

    def test_asymmetric_play(self):
        self.reset_player_color()
        mplayer_1, board, hand, tiles = self.setup()
        mplayer_1.set_strategy(Strategy.LEAST_SYM)

        tile = mplayer_1.play_turn(board, hand, 15)
        tiles.sort(key = lambda x: x.get_sym_score(), reverse=True)
        self.assertTrue(tile == (init_tile_3()))


    def setup2(self, strategy):
        server = Server.Server.reset_get_instance()
        self.reset_player_color()
        mplayer_1 = init_player_john()
        hand = Hand()
        board = Board()
        server.board = board
        loc = (0,1,4)
        mplayer_1.place_pawn(board)
        mplayer_1.loc = Player_location(loc)
        mplayer_1.set_strategy(strategy)

        splayer = SPlayer("red", True, loc)
        splayer.hand = hand
        splayer.player = mplayer_1
        server.splayers_active.append(splayer)

        tile_1 = init_tile_1()
        hand.add_tile(tile_1)
        tile = mplayer_1.play_turn(board, hand, 15)

        return tile, tile_1

    def test_random_play_all_killing(self):
        tile, tile_1 = self.setup2(Strategy.RANDOM)
        self.assertTrue(tile.equal(tile_1))

        
    def test_symmetric_play_all_killing(self):
        tile, tile_1 = self.setup2(Strategy.MOST_SYM)
        self.assertTrue(tile.equal(tile_1))

    def test_asymmetric_play_all_killing(self):
        tile, tile_1 = self.setup2(Strategy.LEAST_SYM)
        self.assertTrue(tile.equal(tile_1))