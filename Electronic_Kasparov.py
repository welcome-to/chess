from random import choice
from board import *
from operations import *


class GameBrains(object):
	def __init__(self,color):
		self.color = color
	def makemove(self,board):
		
		pos_moves = possible_moves(board,self.color,None)
		is_kamikadze = iskamikadze(board)
		pos_moves_filterd = list(filterfalse(is_kamikadze, pos_moves))

		move = choice(pos_moves_filterd)
		return(move[0],move[1])
class iskamikadze(object):
	def __init__(self,board):
		self.board = board
	def __call__(self,move):
		return IsKamikadze(self.board,move[0])(move[1])







