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
        if move is not None and move.after_conversion is not None:
            type=move.after_conversion
        else:
            type=None
        # why not return Move?
        return(move.start,move.end,type)
