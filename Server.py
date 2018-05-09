
from Tile import *
from SPlayer import *
from Board import *
from Deck import *
from Player import *
from MPlayer import *

from Log import *

from copy import copy


class Server():
    __server = None
    available_colors = ["blue", "red", "green", "orange", "sienna", "hotpink", "darkgreen", "purple"]
    all_colors = copy(available_colors)

    def get_instance():
        if Server.__server == None:
            Server()
        return Server.__server

    def reset_get_instance(): # only for testing
        Server.__server = None
        Server.available_colors = copy(Server.all_colors)
        Server()
        return Server.__server

    def __init__(self):
        if self.__server == None:
            self.board = Board()
            self.deck = Deck()
            self.splayers_active = []
            self.splayers_out = []
            self.dragon_owner = None
            Server.__server = self
        else:
            raise Exception("This class is a singleton! use get_instance() for access")


    def build_deck(self):
        self.deck.init()

    # create and initilize splayers from a list of players (human or machine)
    # if human players fails/cheats, it will be replaced by a random machine player
    def init_splayers(self, players):
        num_players = len(players)
        assert(1 < num_players <=8)
        for player in players:
            color = self.available_colors.pop()
            player.initialize(color, self.all_colors)
            new_sp = SPlayer(color)

            # set pawn locatoin
            pawn_loc = player.place_pawn(self.board)
            if not Player_location.check_pawn(pawn_loc):
                eprint("Player pawn loc is invalid")
                player = self.create_bot(new_sp)
                pawn_loc = player.place_pawn()
                if Player_location.check_pawn(pawn_loc):
                    raise Exception("bot is broken ... idk")

            new_sp.player = player
            new_sp.set_location(pawn_loc)
            self.board.add_player(new_sp)
            self.splayers_active.append(new_sp)

            # give starting hand
            for i in range(3):
                new_sp.add_hand(self.deck.pop_tile())


    def start_game(self):
        winners = False
        while not winners:
            if len(self.splayers_active) == 0:
                raise Exception("Server::start_game: active players are empty")
            debug("Remaining players are: ")
            for sp in self.splayers_active:
                hand_num = sp.get_hand_size()
                dragon_msg = ""
                if self.dragon_owner == sp:
                    dragon_msg = ", with dragon"
                debug("\t" + str(sp.get_id()) + " , with " + str(hand_num) + " tiles"+ dragon_msg)


            active_player = self.splayers_active[0]
            id = active_player.get_id()
            if active_player.is_hand_empty():
                raise Exception("Server::start_game: active player " + str(id) + " has ZERO hand")
            move = active_player.player.play_turn(self.board, active_player.get_hand(), self.deck.get_num())
            _, _, _, _, winners = self.play_a_turn(self.deck, self.splayers_active, self.splayers_out, self.board, move)

        # game over
        debug("-------Game Over------")
        debug(str(self.board.get_num()) + " tiles on the board")
        debug("Winners are:")
        for winner in winners:
            debug("\t" + str(winner.get_id()))

        debug("\n\nNot lucky enough: ")
        for sad in self.splayers_out:
            debug("\t" + str(sad.get_id()))
        debug("----------------------")

    # checks if the proposed move by a player(machine/human) is legal
    # expects the player has an associated splayer in server and colors match
    def check_legal_play(self, tile, player):
        cur_splayer = self.find_splayer_from_player(player)
        return self.legal_play(cur_splayer, self.board, tile)

    # return bool
    # assume the board is the correct board
    def legal_play(self, splayer, in_board, tile):
        # is player alive?
        if splayer.is_alive() == False:
            return False
        # is tile a legal tile? (one of the 35 tiles)
        if tile.is_legal_tile() == False:
            return False
        # the tile should not have been on board
        if in_board.has_tile(tile):
            # debug("Server::legal_play board.legal_play fails due to board has tile")
            return False
        # does it belong to the player
        if splayer.possess_tile(tile) == False:
            # debug("Server::legal_play board.legal_play fails due to no possession")
            return False
        # will the path kill the player?
        if in_board.legal_play(tile,splayer) == False:
            # debug("Server::legal_play board.legal_play fails as killed")
            return False
        return True

    # returns, after a turn, deck, splayers_active, splayers_out, board, end_of_game? or winner
    # assume game is not over yet
    # updates the state of the game after the new_tile is placed
    def play_a_turn(self, deck, splayers_active, splayers_out, board, new_tile):
        active_splayer = splayers_active[0]
        id = active_splayer.id
        debug("\nIN " + str(id) + "\'s turn:")
        # replace active_player with bot if move is not legal or it has cheated
        if not self.legal_play(active_splayer, board, new_tile) or active_splayer.get_cheated():
            # replacing player with a random machine player
            bot = self.create_bot(active_splayer)
            active_splayer.player = bot
            new_tile = bot.play_turn(board, active_splayer.get_hand(), deck.get_num())
            if not self.legal_play(active_splayer, board, new_tile):
                # debug("the move is " + str(new_tile.id) + " rot = " + str(new_tile.rotation))
                raise Exception("Bot is broken ... bye")

        # place new_tile
        tile_loc = active_splayer.get_empty_spot()
        board.place_tile(new_tile, tile_loc)
        debug("\t" + str(id) + " places " + str(new_tile) + " at " + str(tile_loc))

        active_splayer.sub_hand(new_tile)

        # iteratively move each player
        temp_out = []
        for sp in splayers_active:
            new_loc, out = board.walk_player(sp)
            if out == True:
                temp_out.append(sp)
            board.move_player(sp, new_loc)
        debug("knocking out: " + str(list(map(lambda x: x.get_id(), temp_out))))
        debug(str(board.num_tiles) + " are on board")


        # remove temp_out from splayers_active
        for op in temp_out:
            if op == self.dragon_owner:
                index = splayers_active.index(op)
                index = (index + 1) % len(splayers_active)
                self.dragon_owner = splayers_active[index]

            splayers_out.append(op)
            splayers_active.remove(op)
            op.set_alive(False)
            op.return_hand(deck)    # return hand to deck

        # check whether game is over
        winners, over = self.game_over(splayers_active, board, temp_out)
        if over == True:
            map(lambda sp: splayers_out.remove(sp), winners)
            return deck, splayers_active, splayers_out, board, winners
        else:
            # TODO: add test for when the player has dragon gets eliminatd
            # dragon should go to the player after the previous dragon owner

            # game is not over
            deck.shuffle()
            draw_order = []
            # determine drawing order
            if deck.has_dragon():
                # no player has the dragon
                draw_order = copy(splayers_active)
            else:
                # start from the dragon owner
                index = splayers_active.index(self.dragon_owner)
                draw_order = splayers_active[index:] + splayers_active[0:index]

            # move the active player to the end
            if active_splayer.is_alive():
                splayers_active.remove(active_splayer)
                splayers_active.append(active_splayer)

            cur_player = draw_order[0]
            while not self.all_player_hand_full(draw_order) and not (deck.is_empty() and not deck.has_dragon()):
                # if the current player is the dragon owner, return it to deck
                if self.dragon_owner == cur_player:
                    self.dragon_owner = None
                    deck.return_dragon()

                # draw one tile from deck
                get_dragon = cur_player.draw_tile(deck)
                if get_dragon:
                    self.dragon_owner = cur_player
                    break

                # update the next player to draw
                cur_player = self.get_next_drawing_player(draw_order, cur_player)

            return deck, splayers_active, splayers_out, board, False


    def game_over(self, splayers_active, board, players_out_in_last_turn):
        # if a move kills all active players, those active players are all winners
        # if a move resulted in one player left, that player is the winner
        # if all tiles are on board (all 35), i.e., every player has empty hand, all active players are winners
        # TODO: add test for all remaining player eliminated at 35th tile
        l = len(splayers_active)
        over = False
        winners = []
        if l == 0:
            over = True
            winners = copy(players_out_in_last_turn)
        elif l == 1 or board.get_num() == 35:
            over = True
            winners = copy(splayers_active)
        return winners, over

    def all_player_hand_full(self, draw_order):
        for sp in draw_order:
            if sp.is_hand_full() == False:
                return False
        return True

    def get_next_drawing_player(self, draw_order, cur_player):
        index = (draw_order.index(cur_player) + 1) % len(draw_order)
        return draw_order[index]

    def find_splayer_from_player(self, player):
        # debug("Server::find_splayer_from_player: " + player.color)
        for splayer in self.splayers_active:
            if splayer.player == player:
                if not (splayer.get_id()== player.color and self.all_colors == player.all_players_color):
                    splayer.set_cheated(True)
                return splayer
        raise Exception("SERVER: in find_splayer_from_player, cannot find given player")

    def create_bot(self, active_splayer):
        name = "bot_" + str(active_splayer.get_id())
        debug(name + " is created")
        active_splayer.set_cheated(False)
        rmplayer = MPlayer(name)
        rmplayer.set_strategy(Strategy.RANDOM)
        rmplayer.loc = active_splayer.get_location()
        rmplayer.initialize(active_splayer.get_id(), self.all_colors) # all_players_color?, resolve color conflict
        rmplayer.state = Player_state.READY
        return rmplayer
