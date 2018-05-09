
from Server import *
from MPlayer import *

class Tournament():
    def start_tournament():
        num_players = 8
        server = Server.Server.reset_get_instance()
        server.build_deck()
        m_players = [None] * num_players
        for i in range(num_players):
            m_players[i] = MPlayer(str(i))
        server.init_splayers(m_players)
        server.start_game()



if __name__ == "__main__":
    i = 0
    while True:
        if i % 100 == 0:
            print("round " + str(i))
        Tournament.start_tournament()
        i += 1
