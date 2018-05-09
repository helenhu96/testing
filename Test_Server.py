import unittest

from Util import *
from Board import *
from SPlayer import *
from Deck import *
from Hand import *
from Server import *

class Test_Server(unittest.TestCase):
    def test_constructor(self):
        server_0 = Server.get_instance()
        server_1 = Server.get_instance()
        self.assertEqual(server_0, server_1)

        with self.assertRaises(Exception):
            server = Server()

    def test_legal_play(self):
        server = Server.reset_get_instance()
        board = Board()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()

        player_1 = SPlayer(1, False, (0, 2, 4))

        player_1.add_hand(tile_1)
        # player is out
        self.assertFalse(server.legal_play(player_1, board, tile_1))

        # legal move: a move that kills the player but all other moves do so as well
        player_1.alive = True
        self.assertTrue(server.legal_play(player_1, board, tile_1))

        # illegal move: invalid tile
        self.assertFalse(server.legal_play(player_1, board, tile_2))

        # illegal move: tile not in hand
        self.assertFalse(server.legal_play(player_1, board, tile_3))

        # illegal move: a move that kills the player but there is an alternative
        # making an illegal move, specifically where the move is an elimination move,
        # but there are non-elimination moves available
        player_1.add_hand(tile_3)
        self.assertFalse(server.legal_play(player_1, board, tile_3))

        # legal move: moves player to new location without being killed
        player_1.add_hand(tile_4)
        self.assertTrue(server.legal_play(player_1, board, tile_4))

    def test_game_over(self):
        server = Server.reset_get_instance()
        board = Board()
        player_4 = SPlayer(4, False, (2, 5, 2))
        players = []
        players_last_out = [player_4]

        # 0 player left, winners are last out
        self.assertEqual(server.game_over(players, board, players_last_out), (players_last_out, True))

        # 1 player left
        player_1 = SPlayer(1, True, (0, 2, 4))
        players.append(player_1)
        self.assertEqual(server.game_over(players, board, players_last_out), ([player_1], True))

        # board all completely full
        board.num_tiles = 35
        player_2 = SPlayer(2, True, (1, 1, 2))
        players.append(player_2)
        self.assertEqual(server.game_over(players, board, players_last_out), ([player_1, player_2], True))

        # board is not full yet
        board.num_tiles = 34
        player_2 = SPlayer(2, True, (1, 1, 2))
        players.append(player_2)
        self.assertEqual(server.game_over(players, board, players_last_out), ([], False))

    def test_all_player_hand_full(self):
        server = Server.reset_get_instance()
        player_1 = SPlayer(1, True, (0, 2, 4))
        player_4 = SPlayer(4, False, (2, 5, 2))

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        # none full
        players= [player_1, player_4]
        self.assertFalse(server.all_player_hand_full(players))

        # one full
        player_1.add_hand(tile_1)
        player_1.add_hand(tile_3)
        player_1.add_hand(tile_4)
        self.assertFalse(server.all_player_hand_full(players))

        # both full
        player_4.add_hand(tile_5)
        player_4.add_hand(tile_6)
        player_4.add_hand(tile_7)
        self.assertTrue(server.all_player_hand_full(players))

        # one full
        player_1.sub_hand(tile_4)
        self.assertFalse(server.all_player_hand_full(players))

    def test_draw_tiles_1(self):
        # moving where one player has the dragon tile before
        # and no one gets any new tiles
        server = Server.reset_get_instance()
        deck = Deck()
        board = Board()

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        player_1 = SPlayer(1, True, (1, 0, 2))
        player_2 = SPlayer(2, True, (6, 6, 0))
        player_4 = SPlayer(4, True, (2, 5, 2))

        player_1.add_hand(tile_3)
        player_2.add_hand(tile_1)
        player_4.add_hand(tile_4)

        active_players = [player_1, player_2, player_4]
        players_last_out = []

        server.dragon_owner = player_1
        deck.own_dragon = False

        self.assertEqual(server.dragon_owner,player_1)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),1)
        self.assertEqual(player_2.hand.get_num(),1)
        self.assertEqual(player_4.hand.get_num(),1)

        d, sa, so, b, res = server.play_a_turn(deck, copy(active_players),
            copy(players_last_out), board, tile_3)

        self.assertEqual(d.get_num(), 0)
        self.assertEqual(d.tiles, [])
        self.assertEqual(sa, [player_2, player_4, player_1])
        self.assertEqual(so, players_last_out)
        self.assertEqual(player_1.get_location().into_tuple(), (1,1,2))
        self.assertEqual(b.num_tiles, 1)
        self.assertEqual(b.get_tile_by_loc(Tile_location((1,1))), tile_3)
        self.assertEqual(b.get_splayer_by_loc(Player_location((1,1,2))), player_1)
        self.assertFalse(res)

        self.assertEqual(server.dragon_owner,player_1)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),0)
        self.assertEqual(player_2.hand.get_num(),1)
        self.assertEqual(player_4.hand.get_num(),1)


    def test_draw_tiles_2(self):
    # moving where the player that has the dragon tile makes
    # a move that causes an elimination (of another player)
    # the eliminated player does not have remaining tiles
        server = Server.reset_get_instance()
        deck = Deck()
        board = Board()

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        player_1 = SPlayer(1, True, (1, 1, 2))
        player_2 = SPlayer(2, True, (1, 3, 6))
        player_3 = SPlayer(3, True, (5, 5, 6))
        board.matrix_player[1][1][2] = player_1
        board.matrix_player[1][3][6] = player_2
        board.matrix_player[5][5][6] = player_3

        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_2, player_1, player_3]
        players_last_out = [player_4]

        board.place_tile(tile_5,Tile_location((1,1)))
        board.place_tile(tile_4,Tile_location((1,3)))
        board.place_tile(tile_7,Tile_location((5,5)))

        player_2.add_hand(tile_3)
        player_1.hand.num_tiles = 0
        player_3.hand.num_tiles = 1
        server.dragon_owner = player_2
        deck.own_dragon = False

        self.assertEqual(server.dragon_owner, player_2)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),0)
        self.assertEqual(player_2.hand.get_num(),1)
        self.assertEqual(player_3.hand.get_num(),1)

        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)

        self.assertEqual(d.get_num(), 0)
        self.assertEqual(sa, [player_3, player_2])
        self.assertTrue(player_1 in so)
        self.assertFalse(player_2 in so)
        self.assertFalse(player_3 in so)
        self.assertEqual(b.num_tiles, 4)
        self.assertEqual(b.matrix_tile[1][2], tile_3)
        self.assertEqual(b.matrix_player[1][1][2], None)
        self.assertEqual(b.matrix_player[1][2][4], player_2)
        self.assertEqual(player_1.get_location().into_tuple(), (1,3,0))
        self.assertEqual(b.matrix_player[1][3][0], player_1)
        self.assertEqual(b.matrix_player[1][1][2], None)
        self.assertFalse(res)

        self.assertEqual(server.dragon_owner, player_2)
        self.assertFalse(deck.has_dragon())
        self.assertFalse(player_1.is_alive())
        self.assertEqual(player_2.hand.get_num(),0)
        self.assertEqual(player_3.hand.get_num(),1)


    def test_draw_tiles_3(self):
    # moving where the player that has the dragon tile makes
    # a move that causes an elimination (of another player)
    # the eliminated player has 1 tile, another player gets the dragon
        server = Server.reset_get_instance()
        deck = Deck()
        board = Board()

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        player_1 = SPlayer(1, True, (1, 1, 2))
        player_2 = SPlayer(2, True, (1, 3, 6))
        player_3 = SPlayer(3, True, (5, 5, 6))
        board.matrix_player[1][1][2] = player_1
        board.matrix_player[1][3][6] = player_2
        board.matrix_player[5][5][6] = player_3

        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_2, player_1, player_3]
        players_last_out = [player_4]

        board.place_tile(tile_5,Tile_location((1,1)))
        board.place_tile(tile_4,Tile_location((1,3)))
        board.place_tile(tile_6,Tile_location((5,5)))

        player_1.add_hand(tile_7)
        player_2.add_hand(tile_3)
        player_3.hand.num_tiles = 1
        server.dragon_owner = player_2
        deck.own_dragon = False

        self.assertEqual(server.dragon_owner, player_2)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),1)
        self.assertEqual(player_2.hand.get_num(),1)
        self.assertEqual(player_3.hand.get_num(),1)

        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)
        # player 1 killed, returning 1 tile to deck
        # player 2 draws 1 tile, returns dragon
        # player 3 gets dragon
        self.assertEqual(d.get_num(), 0)
        self.assertEqual(sa, [player_3, player_2])
        self.assertTrue(player_1 in so)
        self.assertFalse(player_2 in so)
        self.assertFalse(player_3 in so)
        self.assertFalse(res)

        self.assertEqual(server.dragon_owner, player_3)
        self.assertFalse(deck.has_dragon())
        self.assertFalse(player_1.is_alive())
        self.assertEqual(player_2.hand.get_num(),1)
        self.assertEqual(player_3.hand.get_num(),1)

    def test_draw_tiles_4(self):
    # moving where the player that has the dragon tile makes
    # a move that causes an elimination (of another player)
    # the eliminated player does have remaining tiles
    # remaining players hand become full, dragon goes to deck
        server = Server.reset_get_instance()
        deck = Deck()
        board = Board()

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        player_1 = SPlayer(1, True, (1, 1, 2))
        player_2 = SPlayer(2, True, (1, 3, 6))
        player_3 = SPlayer(3, True, (5, 5, 6))
        board.matrix_player[1][1][2] = player_1
        board.matrix_player[1][3][6] = player_2
        board.matrix_player[5][5][6] = player_3

        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_2, player_1, player_3]
        players_last_out = [player_4]

        board.place_tile(tile_5,Tile_location((1,1)))
        board.place_tile(tile_4,Tile_location((1,3)))
        board.place_tile(tile_7,Tile_location((5,5)))

        player_1.add_hand(tile_7)
        player_1.add_hand(tile_6)
        player_1.add_hand(tile_1)
        player_2.hand.num_tiles = 1
        player_2.add_hand(tile_3)
        player_3.hand.num_tiles = 2
        server.dragon_owner = player_2
        deck.own_dragon = False

        self.assertEqual(server.dragon_owner, player_2)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),3)
        self.assertEqual(player_2.hand.get_num(),2)
        self.assertEqual(player_3.hand.get_num(),2)

        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)
        # player 1 killed, returning 1 tile to deck
        # player 2 draws 1 tile, returns dragon
        # player 3 gets 1 tile, done
        self.assertEqual(d.get_num(), 0)
        self.assertEqual(sa, [player_3, player_2])
        self.assertTrue(player_1 in so)
        self.assertFalse(player_2 in so)
        self.assertFalse(player_3 in so)
        self.assertFalse(res)

        self.assertEqual(server.dragon_owner, None)
        self.assertTrue(deck.has_dragon())
        self.assertFalse(player_1.is_alive())
        self.assertEqual(player_2.hand.get_num(),3)
        self.assertEqual(player_3.hand.get_num(),3)


    def test_draw_tiles_5(self):
        # moving where the player that has the dragon tile makes a move
        # that causes themselves to be eliminated
        # 3 players active -> 1 player died
        # player 1 owns dragon and kills itself and return no tile
        # player 2 has the dragon
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        player_1 = SPlayer(1, True, (1, 2, 7))
        player_2 = SPlayer(2, True, (2, 3, 6))
        player_3 = SPlayer(3, True, (4, 4, 6))

        board.matrix_player[1][2][7] = player_1
        board.matrix_player[2][3][6] = player_2
        board.matrix_player[4][4][6] = player_3

        board.place_tile(tile_3,Tile_location((1,2)))
        board.place_tile(tile_4,Tile_location((2,3)))
        board.place_tile(tile_5,Tile_location((4,4)))

        active_players = [player_1, player_2, player_3]
        players_last_out = []
        player_1.add_hand(tile_6)
        player_2.hand.num_tiles = 1
        player_3.hand.num_tiles = 1

        server.dragon_owner = player_1
        deck.own_dragon = False

        self.assertEqual(server.dragon_owner, player_1)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),1)
        self.assertEqual(player_2.hand.get_num(),1)
        self.assertEqual(player_3.hand.get_num(),1)

        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_6)
        # player 2 and 3 remain
        # player 1 returns no card
        # player 2 gets dragon

        self.assertEqual(sa, [player_2, player_3])
        self.assertEqual(b.get_splayer_by_loc(Player_location((1,1,2))), None)
        self.assertEqual(player_1.get_location().into_tuple(), (1, 1, 7))
        self.assertEqual(player_2.get_location().into_tuple(), (2, 3, 6))
        self.assertEqual(player_3.get_location().into_tuple(), (4, 4, 6))

        self.assertEqual(server.dragon_owner, player_2)
        self.assertFalse(deck.has_dragon())
        self.assertFalse(player_1.is_alive())
        self.assertEqual(player_2.hand.get_num(),1)
        self.assertEqual(player_3.hand.get_num(),1)



    def test_draw_tiles_6(self):
        # moving where the player that has the dragon tile makes a move
        # that causes themselves to be eliminated
        # 3 players active -> 1 player died
        # player 1 owns dragon and kills itself and return 1 tile
        # return dragon to deck
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        player_1 = SPlayer(1, True, (1, 2, 7))
        player_2 = SPlayer(2, True, (2, 3, 6))
        player_3 = SPlayer(3, True, (4, 4, 6))

        board.matrix_player[1][2][7] = player_1
        board.matrix_player[2][3][6] = player_2
        board.matrix_player[4][4][6] = player_3

        board.place_tile(tile_3,Tile_location((1,2)))
        board.place_tile(tile_4,Tile_location((2,3)))
        board.place_tile(tile_5,Tile_location((4,4)))

        active_players = [player_1, player_2, player_3]
        players_last_out = []
        player_1.add_hand(tile_6)
        player_1.add_hand(tile_6)
        player_2.hand.num_tiles = 2
        player_3.hand.num_tiles = 3

        server.dragon_owner = player_1
        deck.own_dragon = False

        self.assertEqual(server.dragon_owner, player_1)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),2)
        self.assertEqual(player_2.hand.get_num(),2)
        self.assertEqual(player_3.hand.get_num(),3)

        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_6)
        # player 2 and 3 remain
        # player 1 returns 1 tile, player 2 draws that tile and has 3
        # dragon back to deck

        self.assertEqual(sa, [player_2, player_3])
        self.assertEqual(b.get_splayer_by_loc(Player_location((1,1,2))), None)
        self.assertEqual(player_1.get_location().into_tuple(), (1, 1, 7))
        self.assertEqual(player_2.get_location().into_tuple(), (2, 3, 6))
        self.assertEqual(player_3.get_location().into_tuple(), (4, 4, 6))

        self.assertEqual(server.dragon_owner, None)
        self.assertTrue(deck.has_dragon())
        self.assertFalse(player_1.is_alive())
        self.assertEqual(player_2.hand.get_num(),3)
        self.assertEqual(player_3.hand.get_num(),3)

    def test_draw_tiles_7(self):
        # moving where a player that does not have the dragon tile makes a move
        # and it causes an elimination of the player that has the dragon tile
        # 3 players active -> 1 player died
        # player 1 owns dragon and gets killed by player 2 and return 1 tile
        # return dragon to deck
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()

        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()
        tile_6 = init_tile_6()
        tile_7 = init_tile_7()

        player_1 = SPlayer(1, True, (1, 1, 5))
        player_2 = SPlayer(2, True, (2, 2, 7))
        player_3 = SPlayer(3, True, (4, 4, 6))

        board.matrix_player[1][1][5] = player_1
        board.matrix_player[2][2][7] = player_2
        board.matrix_player[4][4][6] = player_3

        board.place_tile(tile_3,Tile_location((1,1)))
        board.place_tile(tile_5,Tile_location((2,2)))
        board.place_tile(tile_6,Tile_location((4,4)))

        active_players = [player_2, player_3, player_1]
        players_last_out = []
        player_1.add_hand(tile_7)
        player_2.hand.num_tiles = 2
        player_2.add_hand(tile_4)
        player_3.hand.num_tiles = 3

        server.dragon_owner = player_1
        deck.own_dragon = False

        self.assertEqual(server.dragon_owner, player_1)
        self.assertFalse(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),1)
        self.assertEqual(player_2.hand.get_num(),3)
        self.assertEqual(player_3.hand.get_num(),3)

        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_4)
        # player 2 moves and kills player 1
        # player 1 returns 1 tile, player 2 draws that tile and has 3
        # dragon back to deck
        self.assertEqual(sa, [player_3, player_2])
        self.assertEqual(b.get_splayer_by_loc(Player_location((1,1,2))), None)

        self.assertEqual(server.dragon_owner, None)
        self.assertTrue(deck.has_dragon())
        self.assertFalse(player_1.is_alive())
        self.assertEqual(player_2.hand.get_num(),3)
        self.assertEqual(player_3.hand.get_num(),3)

    def test_draw_tiles_8(self):
        # 2 players active -> 2 players active, not over
        # neither have dragon tiles
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()
        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()

        player_1 = SPlayer(1, True, (1, 0, 2))
        player_2 = SPlayer(2, True, (6, 6, 0))
        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_1, player_2]
        players_last_out = [player_4]

        player_1.hand.num_tiles = 2
        player_1.add_hand(tile_3)
        player_2.hand.num_tiles = 3
        deck.add_tile(tile_1)

        self.assertEqual(server.dragon_owner, None)
        self.assertTrue(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),3)
        self.assertEqual(player_2.hand.get_num(),3)

        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)

        self.assertEqual(server.dragon_owner, None)
        self.assertTrue(deck.has_dragon())
        self.assertEqual(player_1.hand.get_num(),3)
        self.assertEqual(player_2.hand.get_num(),3)



    def test_play_a_turn_1(self):
        # 2 players active -> 2 players active, not over
        # player_1 making a move from the edge
        # need to check location matches and splayers_active in correct order
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()
        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()

        player_1 = SPlayer(1, True, (1, 0, 2))
        player_2 = SPlayer(2, True, (6, 6, 0))
        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_1, player_2]
        players_last_out = [player_4]

        # check deck number
        player_1.hand.num_tiles = 2
        player_1.add_hand(tile_3)
        player_2.hand.num_tiles = 3
        deck.add_tile(tile_1)
        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)
        self.assertEqual(d.get_num(), 0)
        self.assertEqual(d.tiles, [])
        self.assertEqual(sa, [player_2, player_1])
        self.assertEqual(so, players_last_out)
        self.assertEqual(player_1.get_location().into_tuple(), (1,1,2))
        self.assertEqual(player_1.hand.get_num(), 3)
        self.assertEqual(b.num_tiles, 1)
        self.assertEqual(b.get_tile_by_loc(Tile_location((1,1))), tile_3)
        self.assertEqual(b.get_splayer_by_loc(Player_location((1,1,2))), player_1)
        self.assertFalse(res)

    def test_play_a_turn_2(self):
        # 2 player active -> both killed
        # making a move where multiple players are eliminated
        # check whether winner are the two
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()

        player_1 = SPlayer(1, True, (1, 1, 2))
        player_2 = SPlayer(2, True, (1, 3, 7))
        board.matrix_player[1][1][2] = player_1
        board.matrix_player[1][3][7] = player_2

        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_1, player_2]
        players_last_out = [player_4]

        board.place_tile(tile_5,Tile_location((1,1)))
        board.place_tile(tile_4,Tile_location((1,3)))

        player_1.hand.num_tiles = 2
        player_1.add_hand(tile_3)
        player_2.hand.num_tiles = 3
        deck.add_tile(tile_1)
        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)
        self.assertEqual(d.get_num(), 1)
        self.assertEqual(d.tiles, [tile_1])
        self.assertEqual(sa, [])
        self.assertTrue(player_1 in so)
        self.assertTrue(player_2 in so)
        self.assertEqual(b.num_tiles, 3)
        self.assertEqual(b.matrix_tile[1][2], tile_3)
        self.assertEqual(b.matrix_player[1][3][0], player_1)
        self.assertEqual(b.matrix_player[1][1][7], player_2)
        self.assertTrue(player_1 in res)
        self.assertTrue(player_2 in res)

    def test_play_a_turn_3(self):
        # 2 player active -> 1 player active, over
        # check whether the winner is the one left
        # making a move that causes a token to cross multiple tiles
        # making a move where multiple players move at once
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()

        player_1 = SPlayer(1, True, (1, 1, 2))
        player_2 = SPlayer(2, True, (1, 3, 6))
        board.matrix_player[1][1][2] = player_1
        board.matrix_player[1][3][6] = player_2

        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_1, player_2]
        players_last_out = [player_4]

        board.place_tile(tile_5,Tile_location((1,1)))
        board.place_tile(tile_4,Tile_location((1,3)))

        player_1.hand.num_tiles = 2
        player_1.add_hand(tile_3)
        player_2.hand.num_tiles = 3
        deck.add_tile(tile_1)
        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)
        self.assertEqual(d.get_num(), 1)
        self.assertEqual(d.tiles, [tile_1])
        self.assertEqual(sa, [player_2])
        self.assertTrue(player_1 in so)
        self.assertFalse(player_2 in so)
        self.assertEqual(b.num_tiles, 3)
        self.assertEqual(b.matrix_tile[1][2], tile_3)
        self.assertEqual(b.matrix_player[1][1][2], None)
        self.assertEqual(b.matrix_player[1][2][4], player_2)

        self.assertEqual(player_1.get_location().into_tuple(), (1,3,0))
        self.assertEqual(b.matrix_player[1][3][0], player_1)
        self.assertEqual(b.matrix_player[1][1][2], None)
        self.assertFalse(player_1 in res)
        self.assertTrue(player_2 in res)

    def test_play_a_turn_4(self):
        # 2 players active -> 2 players active, over, all 35 tiles on board
        # check winner
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()
        tile_1 = init_tile_1()
        tile_2 = init_tile_2()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()

        player_1 = SPlayer(1, True, (2, 2, 4))
        player_2 = SPlayer(2, True, (2, 4, 6))
        board.matrix_player[2][2][4] = player_1
        board.matrix_player[2][4][6] = player_2

        player_4 = SPlayer(4, False, (2, 5, 2))
        active_players = [player_1, player_2]
        players_last_out = [player_4]

        board.place_tile(tile_4,Tile_location((1,2)))
        board.place_tile(tile_1,Tile_location((2,4)))
        board.num_tiles = 34

        player_1.hand.num_tiles = 2
        player_1.add_hand(tile_3)
        player_2.hand.num_tiles = 3
        deck.add_tile(tile_1)
        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_3)
        self.assertEqual(d.get_num(), 1)
        self.assertEqual(d.tiles, [tile_1])
        self.assertEqual(sa, [player_1, player_2])
        self.assertEqual(so, [player_4])
        self.assertEqual(b.num_tiles, 35)
        self.assertEqual(b.matrix_tile[3][2], tile_3)
        self.assertTrue(player_1 in res)
        self.assertTrue(player_2 in res)



    def test_play_a_turn_5(self):
        # 2 players active -> 2 players active, not over
        # making a move where the tile is not placed in its original Location (i.e., it is rotated)
        # need to check location matches and splayers_active in correct order
        server = Server.reset_get_instance()
        board = Board()
        deck = Deck()
        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()

        player_1 = SPlayer(1, True, (1, 1, 2))
        player_2 = SPlayer(2, True, (6, 6, 0))
        player_4 = SPlayer(4, False, (4, 5, 2))
        active_players = [player_1, player_2]
        players_last_out = [player_4]

        board.place_tile(tile_5,Tile_location((1,1)))
        board.place_tile(tile_3,Tile_location((6,6)))
        tile_4.set_rotation(1)

        # check deck number
        player_1.hand.num_tiles = 2
        player_1.add_hand(tile_4)
        player_2.hand.num_tiles = 3
        deck.add_tile(tile_1)
        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_4)
        self.assertEqual(d.get_num(), 0)
        self.assertEqual(d.tiles, [])
        self.assertEqual(sa, [player_2, player_1])
        self.assertEqual(so, players_last_out)
        self.assertEqual(player_1.get_location().into_tuple(), (1,2,3))
        self.assertEqual(player_1.hand.get_num(), 3)
        self.assertEqual(b.num_tiles, 3)
        self.assertEqual(b.get_tile_by_loc(Tile_location((1,2))), tile_4)
        self.assertEqual(b.get_splayer_by_loc(Player_location((1,2,3))), player_1)
        self.assertFalse(res)

    def test_bot_when_not_legal_play(self):
        # 2 players active -> 2 players active, not over
        # making a move where the tile is not placed in its original Location (i.e., it is rotated)
        # need to check location matches and splayers_active in correct order
        server = Server.reset_get_instance()
        board = Board()
        server.board = board
        deck = Deck()
        tile_1 = init_tile_1()
        tile_3 = init_tile_3()
        tile_4 = init_tile_4()
        tile_5 = init_tile_5()

        player_1 = SPlayer("red", True, (1, 1, 2))
        player_2 = SPlayer(2, True, (6, 6, 0))
        player_4 = SPlayer(4, False, (4, 5, 2))
        active_players = [player_1, player_2]
        server.splayers_active = copy(active_players)
        players_last_out = [player_4]

        board.place_tile(tile_5,Tile_location((1,1)))
        tile_4.set_rotation(1)

        # check deck number
        player_1.hand.num_tiles = 0
        player_1.add_hand(tile_3)
        player_2.hand.num_tiles = 3
        deck.add_tile(tile_1)
        self.assertEqual(player_1.player, None)
        d, sa, so, b, res= server.play_a_turn(deck, copy(active_players), copy(players_last_out), board, tile_4)
        self.assertEqual(player_1.player.name, "bot_red")

