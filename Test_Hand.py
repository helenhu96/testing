import unittest

from Util import *
from Hand import *
from Tile import *

class Test_Hand(unittest.TestCase):
    def test_constructor(self):
        hand_1 = Hand()
        self.assertEqual(hand_1.get_num(),0)
        self.assertEqual(hand_1.get_tiles(),[])

    def test_edit_hand(self):
        hand_1 = Hand()
        tile_1 = init_tile_1()
        hand_1.add_tile(tile_1)
        self.assertEqual(hand_1.get_num(),1)
        self.assertTrue(hand_1.has_tile(tile_1))

        hand_1.sub_tile(tile_1)
        self.assertEqual(hand_1.get_num(),0)

        res = hand_1.add_tile(None)
        self.assertTrue(res)

        tile_2 = init_tile_2()
        with self.assertRaises(Exception):
            hand_1.add_tile(tile_2)

    def test_return_to_deck(self):
        deck = Deck()
        hand_1 = Hand()
        tile_1 = init_tile_1()
        tile_2 = init_tile_3()
        hand_1.add_tile(tile_1)
        hand_1.add_tile(tile_2)
        self.assertEqual(hand_1.get_num(), 2)

        hand_1.return_to_deck(deck)
        self.assertEqual(hand_1.get_num(), 0)
        self.assertEqual(hand_1.tiles, [])

    def test_enumerate_tiles(self):
        hand_1 = Hand()
        tile_1 = init_tile_1()
        tile_2 = init_tile_3()
        hand_1.add_tile(tile_1)
        hand_1.add_tile(tile_2)

        res = hand_1.enumerate_tiles(tile_1)
        self.assertEqual(len(res),7)
        for i in range(7):
            if i < 3:
                self.assertEqual(res[i].get_rotation(), i+1)
                self.assertEqual(res[i].paths, tile_1.paths)
            else:
                self.assertEqual(res[i].get_rotation(), i-3)
                self.assertEqual(res[i].paths, tile_2.paths)
