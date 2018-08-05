from board import Board, Coordinates, Move, figures_on_board
from const import *
from operations import possible_moves_from_position

import copy


def decode_move(short_line, board, player_color):
    if short_line == 'O-O':
        return 'e1g1' if player_color == WHITE else 'e8g8'

    if short_line == 'O-O-O':
        return 'e1c1' if player_color == WHITE else 'e8c8'

    # FIXME: add checks that +, #, x are correct: really suspense, or gameover, or figure eaten
    # and exceptions
    is_checkmate = False
    is_check = False
    if short_line[-1] == '#':
        is_checkmate = True
        short_line = short_line[:-1]
    elif short_line[-1] == '+':
        is_check = True
        short_line = short_line[:-1]

    is_conversion = False
    if short_line[-1] in ['Q', 'R', 'N', 'B']:
        is_conversion = True
        short_line = short_line[:-1]

    end_field = short_line[-2:]
    short_line = short_line[:-2]

    is_eating = False
    if short_line and short_line[-1] == 'x':
        is_eating = True
        short_line = short_line[:-1]

    initial_x = None
    initial_y = None
    if short_line:
        if short_line[-1] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            initial_x = short_line[-1]
            short_line = short_line[:-1]
        elif short_line[-1] in ['1', '2', '3', '4', '5', '6', '7', '8']:
            initial_y = short_line[-1]
            short_line = short_line[:-1]

    if not short_line:
        figure_type = PAWN
    else:
        figure_type = {'p': PAWN, 'K': KING, 'Q': QUEEN, 'N': KNIGHT, 'B': BISHOP, 'R': ROOK}[short_line[-1]]

    candidates = figures_on_board(board, type=figure_type, color=player_color)
    if initial_x:
        candidates = list(filter(lambda item: item[1].x == INDEX_TO_LETTER(initial_x), candidates))
    elif initial_y:
        candidates = list(filter(lambda item: item[1].y == initial_y - 1, candidates))

    final_pos = Coordinates.from_string(end_field)
    candidates = list(filter(
        lambda item: final_pos in possible_moves_from_position(board, item[1], player_color, None),
        candidates
    ))

    if not candidates:
        raise RuntimeError("No suitable figures for turn")
    if len(candidates) > 1:
        raise RuntimeError("Too many suitable figures for turn")
    return str(candidates[0][1]) + end_field
