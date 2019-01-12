from random import choice
from board import *
from operations import possible_moves,commit_move,game_status
from common_operations import another_color
from const import *
from castling_moves import fields_under_attack


class GameBrains(object):
    def __init__(self,color,def_cost=0.7,atack_cost=0.05,figure_set_cost=1, enemy_figure_set_cost=1):
        self.color = color
        self.def_cost = def_cost
        self.atack_cost = atack_cost
        self.figure_set_cost = figure_set_cost
        self.enemy_figure_set_cost = enemy_figure_set_cost
    def get_move(self,board,last_move):
        pos_moves = possible_moves(board,self.color,last_move)
        curent_max = -999
        curen_opt_move = [choice(pos_moves)]

        for move in pos_moves:

            back_move = commit_move(move,board,last_move,self.color)
            mesure = self.calc_board(board,self.color)
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
    def calc_board(self,board,color):
        sum_self_color = 0
        sum_another_color = 0
        self_figure_set = figures_on_board(board,color=color)
        enemy_figure_set = figures_on_board(board,color=another_color(color))
        for figure in self_figure_set:
            sum_self_color += FIGURE_COST[figure[0].type] * self.figure_set_cost 
        for figure in figures_on_board(board,color=another_color(color)):
            sum_another_color += FIGURE_COST[figure[0].type] * self.enemy_figure_set_cost
        under_atack_my = 0
        under_atack_enemy = 0
        enemy_fields_under_atack_list = fields_under_attack(board,color)
        fields_under_attack_list =fields_under_attack(board,another_color(color)) 
        for tup in enemy_figure_set:
            if tup[1] in enemy_fields_under_atack_list:
                under_atack_enemy += FIGURE_COST[tup[0].type] * self.atack_cost
        for tup in self_figure_set:
            if tup[1] in fields_under_attack_list:
                under_atack_my += FIGURE_COST[tup[0].type] * self.def_cost 
        return sum_self_color - sum_another_color + under_atack_enemy - under_atack_my