from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove
from fucking_cord_const import *
from common_operations import another_color, NotBeatingSameColor
from possible_moves import *
from functools import reduce


def fields_under_attack(board, enemy_color):
    attacked = [possible_common_moves_from_position(board, item[1], enemy_color) for item in figures_on_board(board, color=enemy_color)]
    # FIXME: e_p_moves
    return reduce(lambda x,y: set(x) | set(y), attacked, set())




def possible_common_moves_from_position(board, position, player_color):
    figure = board.figure_on_position(position)

    if figure is None:
        return []

    type_to_handler = {
        PAWN: raw_possible_moves_pawn,
        ROOK: raw_possible_moves_rook,
        KNIGHT: raw_possible_moves_knight,
        BISHOP: raw_possible_moves_bishop,
        QUEEN: raw_possible_moves_queen,
        KING: raw_possible_moves_king
    }
    given_args = {
        PAWN: [position,board],
        ROOK: [position,board],
        KNIGHT: [position],
        BISHOP: [position,board],
        QUEEN: [position,board],
        KING: [position]
    }

    not_beating_same_color = NotBeatingSameColor(board, position)

    moves = type_to_handler[figure.type](*given_args[figure.type])
    moves = list(filter(not_beating_same_color, moves))

    return moves
