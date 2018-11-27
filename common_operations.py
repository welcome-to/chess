from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove
from fucking_cord_const import *






def is_pawn_moved(board,move):
    figure = board.figure_on_position(move.end)
    if figure is not None and figure.type == PAWN:
        return True
    return False

def another_color(color):
    return WHITE if color == BLACK else BLACK


def is_pawn_jump(board, move, color):
    figure = board.figure_on_position(move.end)
    if figure is None or figure.color != color:
        raise InternalError("This could not happen")
    if figure.type != PAWN:
        return False

    return (color == WHITE and move.end.y - move.start.y == 2) or (color == BLACK and move.end.y - move.start.y == -2)

class NotBeatingSameColor(object):
    def __init__(self, board, initial_position):
        figure = board.figure_on_position(initial_position)
        assert(figure is not None)
        self.color = figure.color
        self.board = board

    def __call__(self, final_position):
        if self.board.figure_on_position(final_position) is None:
            return True
        return self.board.figure_on_position(final_position).color != self.color

