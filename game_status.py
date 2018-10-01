from board import Board
from copy import deepcopy


class GameCondition(object):
    def __init__(self, game_type, player1, player2):
        self.game_type = game_type
        self.player1 = player1
        self.player2 = player2
        self.board_list = []
        self.idle_moves = 0

    def add_move_info(self, board, is_move_idle):
        self.idle_moves = self.idle_moves + 1 if is_move_idle else 0

        for i in self.board_list:
            if board == i[0]:
                i[1] += 1
                return

        self.board_list.append(((deepcopy(board), 1)))
