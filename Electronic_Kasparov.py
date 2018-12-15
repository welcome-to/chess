from random import choice
from board import *
from operations import possible_moves


class GameBrains(object):
    def __init__(self,color):
        self.color = color
    def get_move(self,board,last_move):
        pos_moves = possible_moves(board,self.color,last_move)
        move = choice(pos_moves)
        print("Kasparov says ", move)
        return(move.start,move.end)





