from board import Board, Move
from const import *
from exception import InvalidMove, InternalError, NotImplementedError
from operations import *
from common_operations import is_pawn_moved, another_color, is_pawn_conversion
from Electronic_Kasparov import GameBrains
from game_status import *

import os
import sys

from copy import deepcopy
from datetime import datetime



class GameProcessor(object):
    def __init__(self):
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
    def make_move(self, start, end, figure_to_create=None):
        if self.is_game_over():
            raise RuntimeError("Game over")

        print("Make move: ", start, end, " player: ", self.current_player)

        try:
            #FIXME
            if is_pawn_conversion(self.board,start,end):
                if figure_to_create is None:
                    figure_to_create = QUEEN
            move = create_move(start, end, self.board, self.current_player, figure_to_create)
            has_pawn_moved = is_pawn_moved(self.board, move)
            if is_kamikadze(self.board, move, self._last_move()):
                self.technical_winner = another_color(self.current_player)
            commit_move(move,self.board, self._last_move(), self.current_player)
            self.turns.append(move)
            self.game_condition.add_move_info(self.board, not has_pawn_moved)
            self._update_game_status()
        except Exception as exc:
            print(exc, file=sys.stderr)
            self._run_technical_defeat()

        self.current_player = another_color(self.current_player)

    def _update_game_status(self):
        self.game_status = game_status(self.board, another_color(self.current_player), self._last_move())
        if not self.is_game_over():
            if satisfies_tie_conditions(self.game_condition):
                self.game_status = POSSIBLE_TIE

    def current_allowed_moves(self):
        return list(map(str,possible_moves(self.board,self.current_player,self._last_move())))

    def game_result(self):
        if self.technical_winner is not None:
           return WINNER_BY_COLOR[self.technical_winner]
        return self.game_status

    def is_game_over(self):
        if self.technical_winner is not None:
            return True
        if self.game_status is None or self.game_status == POSSIBLE_TIE:
            return False
        return True

    def is_tie_possible(self):
        return self.technical_winner is None and self.game_status == POSSIBLE_TIE

    def _last_move(self):
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
        GameProcessor =  GameProcessor()
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
