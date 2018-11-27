from board import Board, Move
from const import *
from exception import InvalidMove, InternalError, NotImplementedError
from operations import allowed_moves, is_kamikadze, game_status, create_move, commit_move
from common_operations import is_pawn_moved, another_color
from Electronic_Kasparov import GameBrains
from game_status import *

import os

from copy import deepcopy
from datetime import datetime



class GameProcessor(object):
    def __init__(self,game_mode): # FIXME: game_mode
        self.board = Board()
        self.log = False
        self.boards = []
        self.turns = []
        self.game_condition = GameCondition()
        # outside make_turn `current player' is the one whose turn is next
        self.current_player = WHITE

        self.technical_winner = None
        self.game_status = None

    # `start, end' are two Coordinates objects
    def make_move(self, start, end):
        if self.game_result() is not None:
            raise RuntimeError("Game over")

        print("Make move: ", start, end, " player: ", self.current_player)
        try:
            move = create_move(start, end, self.board, self.current_player)
            if is_kamikadze(self.board, move, self.last_move()):
                self.technical_winner = another_color( self.current_player)
            commit_move(move,self.board,self.last_move(),self.current_player)
            convert_pawns(self.board)
            self.turns.append(move)
            self.game_condition.add_move_info(self.board,not is_pawn_moved(self.board,move))
            self.update_game_status()
        except:
            self._run_technical_defeat()



        self.current_player = another_color(self.current_player)

    def update_game_status(self):  
        self.game_status = game_status(self.board, another_color(self.current_player), self.last_move())
        if self.game_status is None:
            if satisfies_tie_conditions(self.game_condition):
                self.game_status = TIE
    def cur_allowed_moves(self):
        return list(map(str,allowed_moves(self.board,self.current_player,self.last_move())))


    def game_result(self):
        if self.technical_winner is not None:
            return self.technical_winner # dirty
        return self.game_status

    def last_move(self):
        result = None
        if self.turns:
            result = self.turns[-1]
        return result

    def _run_technical_defeat(self):
        self.technical_winner = another_color(self.current_player)
        print("Invalid move. Winner: {0}".format(self.technical_winner))

    def savelog(self,bool):
        self.log = bool
        if self.log:
            if not os.path.exists(LOGDIR):
                os.mkdir(LOGDIR)
            self.log_file = open(
                os.path.join(LOGDIR, LOG_FILE_PATTERN.format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))), 'w'
            )
    @staticmethod
    def loadfromGC(dir):
        GC = load_from_file(dir)
        GameProcessor =  GameProcessor(GC.game_type)
        GameProcessor.log = GC.log
        GameProcessor.current_player = GC.current_player
        GameProcessor.board = GC.current_board
        GameProcessor.GameCondition = GC
        return GameProcessor




def print_result(game_result):
    print({
        0: "White win!",
        1: "Black win!",
        2: "Tie!"
    }[game_result])
