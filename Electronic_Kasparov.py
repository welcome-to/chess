from random import choice
from board import *
from operations import *


class GameBrains(object):
	def __init__(self,color):
		pass
	def makemove(self,board,color):
		self.color = color
		pos_moves = possible_moves(board,self.color,None)
		move = choice(pos_moves)
		return(move[0],move[1])



