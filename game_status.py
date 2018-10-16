from board import Board
from const import *
from pickle import dump, load
from operations import another_color

from copy import deepcopy


class GameCondition(object):
    def __init__(self, game_type, player1, player2,log):
        # FIXME: move away to gui
        self.game_type = game_type
        self.player1 = player1
        self.player2 = player2
        self.board_list = []
        self.idle_moves = 0
        self.current_player = WHITE
        self.current_board = []
        self.log = log

    def add_move_info(self, board, is_move_idle):
        self.idle_moves = self.idle_moves + 1 if is_move_idle else 0
        self.current_player = another_color(self.current_player)
        self.current_board = board

        for i in self.board_list:
            if board == i[0]:
                i[1] += 1
                return

        self.board_list.append(((deepcopy(board), 1)))


def satisfies_tie_conditions(game_condition):
    return game_condition.idle_moves >= MAX_IDLE_MOVES or \
           list(filter(lambda x, y: y >= MAX_REPETITIONS, game_condition.board_list))



def save_to_file(dir,GC):
    f = open(dir,'wb')
    dump(GC,f)
    f.close
def load_from_file(dir):
    f = open(dir,'rb')
    GC = load(f)
    f.close()
    return GC