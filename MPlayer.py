import random

from abc import ABC, abstractmethod
from Player import *
import Server
from Board import *
from Hand import *
from SPlayer import *
from Location import *
from enum import Enum
from Log import *

class Strategy(Enum):
    RANDOM = 0
    LEAST_SYM = 1
    MOST_SYM = 2

class MPlayer(Player):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.strategy = Strategy.RANDOM
        self.loc = Player_location((2, 2, 2))


    # get-name       ;; -> string
    # ;; Returns the players name
    def get_name(self):
        return self.name

    def set_strategy(self, s):
        if s == Strategy.RANDOM:
            self.strategy = Strategy.RANDOM
        elif s == Strategy.LEAST_SYM:
            self.strategy = Strategy.LEAST_SYM
        elif s == Strategy.MOST_SYM:
            self.strategy = Strategy.MOST_SYM
        else:
            raise ValueError("Invalid strategy: ", s)

    # initialize     ;; color? (listof color?) -> void?
    # ;; Called to indicate a game is starting.
    # ;; The first argument is the player's color
    # ;; and the second is all of the players'
    # ;; colors, in the order that the game will be played.
    def initialize(self, my_color, all_players_color):
        self.check_update_state(Player_state.BORN, Player_state.INITED)
        self.check_input_color(my_color)
        self.color = my_color
        self.all_players_color = all_players_color

    # place-pawn     ;; board? -> pawn-loc?
    # ;; Called at the first step in a game; indicates where
    # ;; the player wishes to place their pawn. The pawn must
    # ;; be placed along the edge in an unoccupied space.
    def place_pawn(self, board):
        self.check_update_state(Player_state.INITED, Player_state.READY)
        empty = False
        while (not empty):
            loc = self.get_random_starting_loc()
            empty = board.get_splayer_by_loc(loc) == None
        self.loc = loc
        return loc

    # play-turn      ;; board? (set/c tile?) natural? -> tile?
    # ;; Called to ask the player to make a move. The tiles
    # ;; are the ones the player has, the number is the
    # ;; count of tiles that are not yet handed out to players.
    # ;; The result is the tile the player should place,
    # ;; suitably rotated.
    def play_turn(self, board, hand, num_deck_tiles):
        self.check_update_state(Player_state.READY, Player_state.READY)
        if hand.get_num() == 0:
            raise Exception("Player " + self.color + " has no hand, blaming ***server***")
        if self.strategy == Strategy.RANDOM:
            return self.random_play(board, hand, num_deck_tiles)
        elif self.strategy == Strategy.MOST_SYM:
            return self.symmetric_play(board, hand, num_deck_tiles)
        elif self.strategy == Strategy.LEAST_SYM:
            return self.asymmetric_play(board, hand, num_deck_tiles)
        else:
            raise Exception("MPlayer " + self.name + " has invalid strategy " + self.strategy)

    # end-game       ;; board? (set/c color?) -> void?
    # ;; Called to inform the player of the final board
    # ;; state and which players won the game.
    def end_game(self, board, winners_color):
        self.check_update_state(Player_state.READY, Player_state.BORN)
        return None


    def random_play(self, board, hand, num_deck_tiles):
        num_tiles = hand.get_num()
        selection_list = [i for i in range(num_tiles*4)]
        tiles = hand.get_tiles()

        done = False

        while not done:
            current = selection_list[random.randint(0, len(selection_list) - 1)]
            selection_list.remove(current)
            tile = tiles[current // 4]
            rotation = current % 4
            tile.set_rotation(rotation)
            server = Server.Server.get_instance()
            if server.check_legal_play(tile, self):
                return tile

    # Less number of different ways to place the tile, more symmetric
    def symmetric_play(self, board, hand, num_deck_tiles):
        return self.play_with_sym_order(board, hand, False)

    # More number of different ways to place the tile, less symmetric
    def asymmetric_play(self, board, hand, num_deck_tiles):
        return self.play_with_sym_order(board, hand, True)

    # Pick a move based on tile's sym_score ranking in (descending/ascending) order
    def play_with_sym_order(self, board, hand, descending):
        num_tiles = hand.get_num()
        tiles = hand.get_tiles()
        selection_list = [i for i in range(num_tiles*4)]
        legal_list = []

        for current in selection_list:
            tile = tiles[current // 4]
            rotation = current % 4
            server = Server.Server.get_instance()
            if server.check_legal_play(tile, self):
                legal_list.append(current)

        legal_list.sort(key = lambda x: tiles[x // 4].get_sym_score(), reverse=descending)

        the_tile = tiles[legal_list[0] // 4]
        the_rotation = legal_list[0] % 4
        the_tile.set_rotation(the_rotation)
        return the_tile

    def get_random_starting_loc(self):
        side = random.randint(0, 3)
        pos = random.randint(1, 6)
        rep = random.randint(0, 1)

        x = y = ep = -1
        if side == 0: #top
            x = 0
            y = pos
            ep = rep + 4 # facing down, 4 or 5
        elif side == 1: #right
            x = pos
            y = 7
            ep = rep + 6 # facing left, 6 or 7
        elif side == 2: #bottom
            x = 7
            y = pos
            ep = rep + 0 # facing up, 0 or 1
        elif side == 3: #left
            x = pos
            y = 0
            ep = rep + 2 # facing right, 2 or 3
        else:
            raise Exception("??? RNG is dead")

        return Player_location((x, y, ep))
