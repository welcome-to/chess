from board import Board, Move
from const import *
from exception import InvalidMove, InternalError, NotImplementedError
from operations import convert_pawns, is_correct, is_castling, is_e_p, game_status, make_castling, make_e_p, another_color
from Electronic_Kasparov import GameBrains

import os

from copy import deepcopy
from datetime import datetime



class GameProcessor(object):
    def __init__(self,game_mode):
        self.board = Board()
        self.game_mode = game_mode
        self.log = False
        self.boards = []
        self.turns = []
        if self.game_mode == ONEPLAYER:
            self.algorithm = GameBrains(BLACK)
        # outside make_turn `current player' is the one whose turn is next
        self.current_player = WHITE

        self.technical_winner = None
        self.game_status = None

    # `start, end' are two Coordinates objects
    def make_move(self, start, end):
        if self.game_result() is not None:
            raise RuntimeError("Game over")

        turn = Move(start, end)

        if not is_correct(turn, self.board, self.current_player, self.last_move()):
            self._run_technical_defeat()
            return
        if is_castling(turn, self.board):
            make_castling(self.board, turn)
        elif is_e_p(turn, self.board):
            make_e_p(self.board, turn)
        else: # move
            self.board.move(turn.start, turn.end)
        convert_pawns(self.board)
        self.boards.append(deepcopy(self.board))
        self.turns.append(deepcopy(turn))

        self.current_player = another_color(self.current_player)

        self.game_status = game_status(self.board, self.current_player, turn)
        if (self.game_status == None) and (self.game_mode == ONEPLAYER) and (self.current_player == BLACK):
            self.nextmove()


    def allowed_moves(self):
        return allowed_moves(board, self.current_player, self.last_move())

    def nextmove(self):
        start,end = self.algorithm.makemove(self.board)
        self.make_turn(start,end)

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



def print_result(game_result):
    print({
        0: "White win!",
        1: "Black win!",
        2: "Tie!"
    }[game_result])
