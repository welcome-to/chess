from board import Board, Move
from const import *
from exception import InvalidMove, InternalError, NotImplementedError
from operations import game_status, is_correct, convert_pawns, make_castling

import os

from copy import deepcopy
from datetime import datetime


class Algorithm(object):
    def __init__(self, name):
        self.name = name

    def make_turn(self, position):
        raise NotImplementedError()


class HumanPlayer(Algorithm):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)

    def __repr__(self):
        return str(self.name)

    def make_turn(self, board):
        line = input()
        return line


class GameProcessor(object):
    def __init__(self):
        self.board = Board()
        self.log = False
        self.boards = []
        self.turns = []
        # outside make_turn `current player' is the one whose turn is next
        self.current_player = WHITE
        self.next_player = BLACK

        self.technical_winner = None

    # `start, end' are two Coordinates objects
    def make_turn(self, start, end):
        try:
            if (str(start)+str(end)) in CASTLING_TYPES.keys():
                turn = Move(start, end, is_roque = True)
            else:
                turn = Move(start, end)
        except:
            self._run_technical_defeat()
            return
        self.turns.append(deepcopy(turn))

        if not is_correct(turn, self.board, self.current_player):
            self._run_technical_defeat()
            return
        if turn.is_roque:
            make_castling(self.board, turn)
        else: # move
            self.board.move(turn.start, turn.end)
        convert_pawns(self.board)
        self.boards.append(deepcopy(self.board))


        self.current_player, self.next_player = self.next_player, self.current_player
        if self.log:
            print(1)
            print(str(command[0]).upper()+str(command[1]).upper())
            self.log_file.write(str(command[0]).upper()+str(command[1]).upper())

    def game_result(self):
        if self.technical_winner is not None:
            return self.technical_winner # dirty
        return game_status(self.board, self.current_player)

    def _run_technical_defeat(self):
        print("Invalid move")
        if self.current_player == WHITE:
            self.technical_winner = BLACK
        else:
            self.technical_winner = WHITE

    # for debug purposes
    def __del__(self):
        print("Destructor called")

    def savelog(self,bool):
        self.log = bool
        if self.log:
            if not os.path.exists(LOGDIR):
                os.mkdir(LOGDIR)
            self.log_file = open(
                os.path.join(LOGDIR, LOG_FILE_PATTERN.format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))), 'w'
            )


def play(first, second):
    gp = GameProcessor()

    current_player = first
    next_player = second

    while gp.game_result() is None:
        print(gp.board)
        print("Player: {0}".format(current_player))
        print("Enter your turn. Example: 'e2 e4' or 'tie'")
        turn = current_player.make_turn(deepcopy(gp.board))
        gp.make_turn(turn)
        current_player, next_player = next_player, current_player

    return gp.game_result()



def print_result(game_result):
    print({
        0: "White win!",
        1: "Black win!",
        2: "Tie!"
    }[game_result])


if __name__ == "__main__":
    first = HumanPlayer("xyu1")
    second = HumanPlayer("xyu2")
    result = play(first, second)
    print_result(result)
