from Electronic_Kasparov import GameBrains as DumbKasparov
from Electronic_Kasparov_2 import GameBrains as SlowDumbKasparov

from game_engine import GameProcessor

from const import *


def run_game(white, black):
    gp = GameProcessor()
    previous_move = None
    players = white, black
    while not gp.is_game_over() and not gp.is_tie_possible():
        start, end, figure = players[0].get_move(gp.board, previous_move)
        gp.make_move(start, end, figure_to_create=figure)
        previous_move = gp.last_move()
        players = players[1], players[0]

    return(gp.game_result())


if __name__ == "__main__":
    result = run_game(DumbKasparov(WHITE), SlowDumbKasparov(BLACK))
    print(result)
