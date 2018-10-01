from board import Board
from copy import deepcopy




class GameCondition(object):
    def __init__(self,game_type,player1,player2):
        self.game_type
        self.player1
        self.player2
        self.board_list = []
        self.last_pawn_move = 0
    def add_board(self,board,pawn_move):
        if pawn_move:
            self.last_pawn_move+=1
        for i in self.board_list:
            if board == i[0]:
                i[1]+=1
                return True
        self.board_list.append((deepcopy((board,1))))