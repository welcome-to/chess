from random import choice
from board import *
from operations import *


class GameBrains(object):
	def __init__(self,color):
		self.color = color
	def makemove(self,board):
		
		pos_moves = possible_moves(board,self.color,None)
		pos_moves_filterd = list(filterfalse(lambda item: IsKamikadze(board, item[0])(item[1]), pos_moves))

		move = choice(pos_moves_filterd)
		return(move[0],move[1])





