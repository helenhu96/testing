import unittest

from Util import *
from Board import *
from SPlayer import *

class Test_Board(unittest.TestCase):
    def init_player_1(self):
        return SPlayer(1, True, (1,1,3))

    def test_change_board(self):
        board = Board()
        tile = init_tile_1()

        with self.assertRaises(Exception):
            board.place_tile(tile, Tile_location((0,0)))
        with self.assertRaises(Exception):
            board.place_tile(tile, Tile_location((0,1)))

        board.place_tile(tile,Tile_location((1,1)))
        self.assertEqual(board.matrix_tile[1][1], tile)

        with self.assertRaises(Exception):
            board.place_tile(tile, Tile_location((1,1)))

        board.remove_tile(Tile_location((1,1)))
        self.assertEqual(board.matrix_tile[1][1], None)

        with self.assertRaises(Exception):
            board.remove_tile(Tile_location((1,1)))

        with self.assertRaises(Exception):
            board.remove_tile(Tile_location((1,7)))

    def test_get_next_tile_loc(self):
        board = Board()

        self.assertEqual(board.get_next_tile_loc((1,1),0), ((0, 1)))
        self.assertEqual(board.get_next_tile_loc((1,1),2), ((1, 2)))
        self.assertEqual(board.get_next_tile_loc((1,1),4), ((2, 1)))
        self.assertEqual(board.get_next_tile_loc((1,1),6), ((1, 0)))
        self.assertEqual(board.get_next_tile_loc((0,1),4), ((1, 1)))
        self.assertEqual(board.get_next_tile_loc((0,1),2), ((0, 2)))

    def test_walk(self):
        board = Board()
        tile_1 = init_tile_3()
        tile_2 = init_tile_4()

        board.place_tile(tile_1, Tile_location((1,1)))

        # out of bound
        loc, a, b = board.walk(Player_location((1,1,0))) 
        self.assertEqual((loc.into_tuple(), a, b), ((1,1,0), True, True))

        # next tile empty
        loc, a, b = board.walk(Player_location((1,1,2)))
        self.assertEqual((loc.into_tuple(), a, b), ((1,1,2), True, False))

        # next tile not empty, but no player is there
        board.place_tile(tile_2, Tile_location((1,2)))
        loc, a, b = board.walk(Player_location((1,1,2)))
        self.assertEqual((loc.into_tuple(), a, b), ((1,2,0), False, False))

    def test_mock_walk_player(self):
        board = Board()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2() # illegal tile
        tile_4 = init_tile_4()

        player_1 = SPlayer(1, True, (0, 2, 5))
        self.assertTrue(board.mock_walk_player(tile_1, player_1))
        self.assertFalse(board.mock_walk_player(tile_2, player_1))

        board.place_tile(tile_1, Tile_location((1,1)))
        self.assertTrue(board.mock_walk_player(tile_2, player_1))
        self.assertFalse(board.mock_walk_player(tile_4, player_1))


    def test_legal_play(self):
        board = Board()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()

        # legal move: a move that kills the player but all other moves does so as well
        player_1 = SPlayer(1, True, (0, 2, 4))
        self.assertTrue(board.legal_play(tile_1, player_1))

        # illegal move: a move that kills the player but there is alternative
        player_1.add_hand(tile_3)
        self.assertFalse(board.legal_play(tile_3, player_1))

        # legal move: moves player to new location without being killed
        player_1.add_hand(tile_4)
        self.assertTrue(board.legal_play(tile_4, player_1))

    def test_move_player(self):
        board = Board()
        player = SPlayer(1, True, (0, 2, 4))

        board.add_player(player)
        self.assertEqual(player.get_location().into_tuple(), (0, 2, 4))
        self.assertEqual(board.matrix_player[0][2][4], player)

        board.remove_player(player)
        self.assertEqual(board.matrix_player[0][2][4], None)

        board.add_player(player)
        board.move_player(player, Player_location((5,5,5)))
        self.assertEqual(player.get_location().into_tuple(), (5, 5, 5))
        self.assertEqual(board.matrix_player[0][2][4], None)
        self.assertEqual(board.matrix_player[5][5][5], player)
