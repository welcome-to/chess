from Electronic_Kasparov import GameBrains as DumbKasparov
from Electronic_Kasparov_2 import GameBrains as SlowDumbKasparov

from game_engine import GameProcessor

from const import *

from copy import deepcopy

from collections import Counter

def run_game(white, black):
    gp = GameProcessor()
    previous_move = None
    players = white, black
    while not gp.is_game_over() and not gp.is_tie_possible():
        start, end, figure = players[0].get_move(deepcopy(gp.board), previous_move)
        gp.make_move(start, end, figure_to_create=figure)
        previous_move = gp.last_move()
        players = players[1], players[0]

    return(gp.game_result())


if __name__ == "__main__":
    result_list = [run_game(SlowDumbKasparov(WHITE), SlowDumbKasparov(BLACK,atack_cost=0.05,def_cost=0.5,figure_set_cost=1,enemy_figure_set_cost=1)) for i in range(int(input('Number of games to test on: ')))]

    print(Counter(result_list).most_common())
