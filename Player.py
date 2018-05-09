from abc import ABC, abstractmethod
from enum import Enum

class Player_state(Enum):
    BORN = 0
    INITED = 1
    READY = 2   

class Player(ABC):
    possible_colors = ["blue", "red", "green", "orange", "sienna", "hotpink", "darkgreen", "purple"]

    def __init__(self):
        super().__init__()
        self.state = Player_state.BORN
        self.name = None
        self.color = None
        self.all_players_color = None


    # get-name       ;; -> string
    # ;; Returns the players name
    @abstractmethod
    def get_name(self):
        pass

    # initialize     ;; color? (listof color?) -> void?
    # ;; Called to indicate a game is starting.
    # ;; The first argument is the player's color
    # ;; and the second is all of the players'
    # ;; colors, in the order that the game will be played.
    @abstractmethod
    def initialize(self, my_color, all_players_color):
        pass

    # place-pawn     ;; board? -> pawn-loc?
    # ;; Called at the first step in a game; indicates where
    # ;; the player wishes to place their pawn. The pawn must
    # ;; be placed along the edge in an unoccupied space.
    @abstractmethod
    def place_pawn(self, board):
        pass

    # play-turn      ;; board? (set/c tile?) natural? -> tile?
    # ;; Called to ask the player to make a move. The tiles
    # ;; are the ones the player has, the number is the
    # ;; count of tiles that are not yet handed out to players.
    # ;; The result is the tile the player should place,
    # ;; suitably rotated.
    @abstractmethod
    def play_turn(self, board, hand, num_deck_tiles):
        pass

    # end-game       ;; board? (set/c color?) -> void?
    # ;; Called to inform the player of the final board
    # ;; state and which players won the game.
    @abstractmethod
    def end_game(self, board, winners_color):
        pass

    def check_input_color(self, color):
        if not color in self.possible_colors:
            raise Exception("Input color " + color + " is not allowed.")

    def check_update_state(self, expected_state, next_state):
        if self.state != expected_state:
            class_name = type(self).__name__ + " should be "
            state_msg = str(expected_state) + ", but is " + str(self.state) + ", "
            blaming_msg = "blaming the ***server***"
            raise Exception(class_name + state_msg + blaming_msg)

        self.state = next_state












