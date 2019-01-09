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
        curen_opt_move = [choice(pos_moves)]

        for move in pos_moves:

            back_move = commit_move(move,board,last_move,self.color)
            print(move)
            mesure = calc_board(board,self.color)
            mesure = mesure[0]-mesure[1]+mesure[2]+mesure[3]
            game_stat = game_status(board,another_color(self.color),move) 

            if game_stat is not None and game_status != TIE:
                curen_opt_move = [move]
                commit_move(back_move,board, last_move, self.color)
                break

            if game_stat != TIE:
                if mesure > curent_max:
                    curent_max = mesure
                    curen_opt_move = [move]
                elif mesure == curent_max:
                    curen_opt_move.append(move)
            commit_move(back_move,board, last_move, self.color)

        move = choice(curen_opt_move)

        print("Kasparov 2.0 says ", move)
        if move.after_conversion is not None:
            type=move.after_conversion
        else:
            type=None
        return(move.start,move.end,type)
def calc_board(board,color):
    sum_self_color = 0
    sum_another_color = 0
    self_figure_set = figures_on_board(board,color=color)
    enemy_figure_set = figures_on_board(board,color=another_color(color))
    for figure in self_figure_set:
        sum_self_color += FIGURE_COST[figure[0].type] 
    for figure in figures_on_board(board,color=another_color(color)):
        sum_another_color += FIGURE_COST[figure[0].type]
    under_atack_my = 0
    under_atack_enemy = 0
    enemy_fields_under_atack_list = fields_under_attack(board,color)
    fields_under_attack_list =fields_under_attack(board,another_color(color)) 
    for tup in enemy_figure_set:
        if tup[1] in enemy_fields_under_atack_list:
            under_atack_enemy += FIGURE_COST[tup[0].type] * 0.1
    for tup in self_figure_set:
        if tup[1] in fields_under_attack_list:
            under_atack_my -= FIGURE_COST[tup[0].type]*0.5
    print('under_atack mesure :'+ str(under_atack))
    print('field cost :' + str(sum_self_color - sum_another_color))
    return sum_self_color, sum_another_color, under_atack_enemy,under_atack_my