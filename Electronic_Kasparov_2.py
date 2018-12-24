from random import choice
from board import *
from operations import possible_moves,commit_move,game_status
from common_operations import another_color
from const import *


class GameBrains(object):
    def __init__(self,color):
        self.color = color
    def get_move(self,board,last_move):
        pos_moves = possible_moves(board,self.color,last_move)
        curent_max = -999
        for move in pos_moves:
            back_move = commit_move(move,board,last_move,self.color)
            mesure = self._calc_board(board)
            if game_status(board,another_color(self.color),move) is not None:
                curen_opt_move = move
                break
            if mesure > curent_max:
                curent_max = mesure
                curen_opt_move = move
            commit_move(back_move,board, last_move, another_color(self.color))
        move = curen_opt_move
        print("Kasparov says ", move)
        if move.after_conversion is not None:
            type=move.after_conversion
        else:
            type=None

        return(move.start,move.end,type)
    def _calc_board(self,board):
        sum_self_color = 0
        sum_another_color = 0
        for figure in figures_on_board(board,color=self.color):
            sum_self_color += FIGURE_COST[figure[0].type] 
        for figure in figures_on_board(board,color=another_color(self.color)):
            sum_another_color += FIGURE_COST[figure[0].type]
        mesure = sum_self_color - sum_another_color
        return mesure