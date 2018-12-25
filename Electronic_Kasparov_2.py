from random import choice
from board import *
from operations import possible_moves,commit_move,game_status
from common_operations import another_color
from const import *
from castling_moves import fields_under_attack


class GameBrains(object):
    def __init__(self,color):
        self.color = color
    def get_move(self,board,last_move):
        pos_moves = possible_moves(board,self.color,last_move)
        curent_max = -999
        curen_opt_move = choice(pos_moves)
        for move in pos_moves:
            back_move = commit_move(move,board,last_move,self.color)
            mesure = self._calc_board(board)
            game_stat = game_status(board,another_color(self.color),move) 
            if game_stat is not None and game_status != TIE:
                curen_opt_move = move
                commit_move(back_move,board, last_move, self.color)
                break
            if game_stat != TIE:
                if mesure > curent_max:
                    curent_max = mesure
                    curen_opt_move = move
            commit_move(back_move,board, last_move, self.color)
        move = curen_opt_move
        print("Kasparov 2.0 says ", move)
        if move.after_conversion is not None:
            type=move.after_conversion
        else:
            type=None
        return(move.start,move.end,type)
    def _calc_board(self,board):
        sum_self_color = 0
        sum_another_color = 0
        self_figure_set = figures_on_board(board,color=self.color)
        enemy_figure_set = figures_on_board(board,color=another_color(self.color))
        for figure in self_figure_set:
            sum_self_color += FIGURE_COST[figure[0].type] 
        for figure in figures_on_board(board,color=another_color(self.color)):
            sum_another_color += FIGURE_COST[figure[0].type]
        under_atack = 0
        enemy_fields_under_atack_list = fields_under_attack(board,self.color)
        fields_under_attack_list =fields_under_attack(board,another_color(self.color))
        if figures_on_board(board,type=KING,color=another_color(self.color))[0][1] in enemy_fields_under_atack_list:
            under_atack += 1 
        '''
        for tup in enemy_figure_set:
            if tup[1] in enemy_fields_under_atack_list:
                under_atack += FIGURE_COST[tup[0].type] * 0.1
        '''
        for tup in self_figure_set:
            if tup[1] in fields_under_attack_list:
                under_atack -= FIGURE_COST[tup[0].type]*0.5
        mesure = sum_self_color - sum_another_color + under_atack
        return mesure