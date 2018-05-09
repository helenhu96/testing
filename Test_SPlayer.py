import unittest

from SPlayer import *

class Test_SPlayer(unittest.TestCase):
    def init_player_1(self):
        return SPlayer(1, True, (0,1,4))

    def test_constructor(self):
        player_1 = self.init_player_1()
        self.assertEqual(player_1.id, 1)
        self.assertTrue(player_1.is_alive())
        self.assertEqual(player_1.get_location().into_tuple(), (0,1,4))
        self.assertEqual(player_1.get_hand().get_num(), 0)

    def test_modifier(self):
        player_1 = self.init_player_1()
        player_1.set_location(Player_location((1,1,1)))
        self.assertEqual(player_1.get_location().into_tuple(), (1,1,1))

        with self.assertRaises(Exception):
            player_1.set_location(Player_location((-1,1,1)))

        with self.assertRaises(Exception):
            player_1.set_location(Player_location((1,1,9)))
        with self.assertRaises(Exception):
            player_1.set_location(Player_location((0,0,9)))

        with self.assertRaises(Exception):
            player_1.set_location(Player_location((1,1)))

    def test_empty_spot(self):
        player_1 = self.init_player_1()

        player_1.set_location(Player_location((1,1,0)))
        with self.assertRaises(Exception):
            player_1.get_empty_spot()

        player_1.set_location(Player_location((0,1,4)))
        self.assertEqual(player_1.get_empty_spot().into_tuple(), (1,1))
