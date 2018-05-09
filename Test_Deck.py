import unittest

from Util import *
from Deck import *

class Test_Deck(unittest.TestCase):
    def test_constructor(self):
        deck = Deck()
        self.assertEqual(deck.get_num(),0)
        self.assertTrue(deck.is_empty())
        self.assertEqual(deck.tiles,[])
        self.assertTrue(deck.has_dragon())

    def test_modifier(self):
        deck = Deck()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2()
        self.assertTrue(deck.has_dragon())

        res = deck.pop_tile()
        self.assertEqual(res, None)
        self.assertFalse(deck.has_dragon())

        deck.add_tile(tile_1)
        deck.add_tile(tile_2)
        self.assertEqual(deck.get_num(), 2)
        self.assertFalse(deck.is_empty())
        self.assertEqual(deck.tiles,[tile_1, tile_2])

        res = deck.pop_tile()
        self.assertTrue(res.equal(tile_2))
        self.assertEqual(deck.get_num(), 1)
        self.assertEqual(deck.tiles,[tile_1])

    def test_equal(self):
        deck1 = Deck()
        deck2 = Deck()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2()

        deck1.add_tile(tile_1)
        deck1.add_tile(tile_2)
        deck2.add_tile(tile_2)
        self.assertFalse(deck1 == deck2)

        deck2.add_tile(tile_1)
        self.assertTrue(deck1 == deck2)
