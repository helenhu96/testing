import unittest

from Util import *
from Tile import *

class Test_Tile(unittest.TestCase):
    def test_constructor(self):
        tile_1 = init_tile_1()
        self.assertEqual(tile_1.id, 1)
        self.assertEqual(tile_1.paths, ((0,1),(2,3),(4,5),(6,7)))
        self.assertEqual(tile_1.rotation, 0)

    def test_legal_tile(self):
        tile_1 = init_tile_1()
        self.assertTrue(tile_1.is_legal_tile())

        tile_2 = init_tile_2()
        self.assertFalse(tile_2.is_legal_tile())

    def test_equal(self):
        tile_1 = init_tile_1()
        another_tile_1 = init_tile_1()
        self.assertTrue(tile_1.equal(another_tile_1))

        tile_2 = init_tile_2()
        self.assertFalse(tile_1.equal(tile_2))

    def test_walk_path(self):
        tile_1 = init_tile_1()
        self.assertEqual(tile_1.walk_path(0),1)

        with self.assertRaises(Exception):
            tile_1.walk_path(10)

    def test_set_rotation(self):
        tile_1 = init_tile_1()
        with self.assertRaises(ValueError):
            tile_1.set_rotation(4)

        tile_1.set_rotation(2)
        self.assertEqual(tile_1.get_rotation(), 2)

    def test_compute_sym_score(self):
        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_6 = init_tile_6()

        self.assertEqual(tile_1.get_sym_score(), 1)
        self.assertEqual(tile_3.get_sym_score(), 4)
        self.assertEqual(tile_4.get_sym_score(), 4)
        self.assertEqual(tile_6.get_sym_score(), 2)
