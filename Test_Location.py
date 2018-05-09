import unittest

from Location import *

class Test_Player_location(unittest.TestCase):
    def test_out_of_bound(self):
        loc_0 = Player_location((1,1,0))
        self.assertTrue(loc_0.out_of_bound())

        loc_1 = Player_location((1,6,2))
        self.assertTrue(loc_1.out_of_bound())

        loc_2 = Player_location((6,3,4))
        self.assertTrue(loc_2.out_of_bound())

        loc_3 = Player_location((3,1,6))
        self.assertTrue(loc_3.out_of_bound())

        loc_4 = Player_location((1,6,5))
        self.assertFalse(loc_4.out_of_bound())