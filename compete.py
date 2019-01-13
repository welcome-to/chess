from Electronic_Kasparov import GameBrains as DumbKasparov
from Electronic_Kasparov_2 import GameBrains as SlowDumbKasparov

from const import *
from game_engine import GameProcessor

from copy import deepcopy
from collections import Counter
from multiprocessing import Process, SimpleQueue
import os


def run_game(white, black, q):
    gp = GameProcessor()
    previous_move = None
    players = white, black
    while not gp.is_game_over() and not gp.is_tie_possible():
        start, end, figure = players[0].get_move(deepcopy(gp.board), previous_move)
        gp.make_move(start, end, figure_to_create=figure)
        previous_move = gp.last_move()
        players = players[1], players[0]

    #return(gp.game_result())
    print("{0} vs {1}: {2} in {3} turns".format(white.player_name, black.player_name, gp.game_result(), gp.game_length()))
    q.put(gp.game_result())

def run_many(white, black, q, how_many):
    for _ in range(how_many):
        run_game(white, black, q)

def processors_number():
    return int(os.popen("cat /proc/cpuinfo | grep -c processor").read().strip())


if __name__ == "__main__":
    """
    result_list = [run_game(
        SlowDumbKasparov(WHITE),
        SlowDumbKasparov(BLACK,atack_cost=0.05,def_cost=0.5,figure_set_cost=1,enemy_figure_set_cost=1)
    ) for i in range(int(input('Number of games to test on: ')))]
    """
    q = SimpleQueue()
    how_many = int(input("Number of games per process? "))

    white = SlowDumbKasparov(WHITE, player_name="ordinary kasparov")
    black = SlowDumbKasparov(BLACK,figure_set_cost=1,enemy_figure_set_cost=1.1, player_name="furious kasparov")
    pp = []
    for _ in range(processors_number()):
        p = Process(target=run_many, args=(white, black, q, how_many))
        p.start()
        pp.append(p)
    for p in pp:
        p.join()
    reuslt_array = []
    while not q.empty():
        reuslt_array.append(q.get())
    print(Counter(reuslt_array).most_common())
    

    
