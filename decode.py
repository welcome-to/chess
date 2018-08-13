from board import Board, Coordinates, Move, figures_on_board
from const import *
from operations import possible_moves_from_position
from run import GameProcessor

import copy
import sys


class DecodeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


def decode_move(short_line, board, player_color):
    if short_line == '0-0':
        return 'e1g1' if player_color == WHITE else 'e8g8'

    if short_line == '0-0-0':
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
        candidates = list(filter(lambda item: item[1].x == LETTER_TO_INDEX[initial_x], candidates))
    elif initial_y:
        candidates = list(filter(lambda item: item[1].y == initial_y - 1, candidates))

    final_pos = Coordinates.from_string(end_field)
    candidates = list(filter(
        lambda item: final_pos in possible_moves_from_position(board, item[1], player_color, None),
        candidates
    ))

    print("\n{0}\n".format(board))
    if not candidates:
        raise RuntimeError("No suitable figures for turn")
    if len(candidates) > 1:
        raise RuntimeError("Too many suitable figures for turn")
    return str(candidates[0][1]) + end_field



def decode_game(line):
    def end_word(line):
        result = line.find(' ')
        if result == -1:
            return len(line)
        return result

    game_results = ['1-0', '0-1', '1/2']
    human_readable = []
    n = 1
    gp = GameProcessor()
    while line:
        print("Turn #{0}".format(n), file=sys.stderr)
        for game_result in game_results:
            if line.startswith(game_result):
                human_readable += [game_result]
                return human_readable
        if gp.game_result() is not None:
            raise DecodeError("Expected end of game")

        prefix = str(n) + '.'
        if not line.startswith(prefix):
            raise DecodeError("Expected turn number: {0}".format(line))
        line = line[len(prefix):]

        line = line.lstrip(' ')
        next_space = end_word(line)
        white_turn = line[:next_space]
        try:
            decoded = decode_move(white_turn, gp.board, WHITE)
        except:
            raise DecodeError("Expected correct move description: `{0}`".format(white_turn))
        human_readable += [decoded]
        gp.make_turn(
            Coordinates.from_string(decoded[:2]),
            Coordinates.from_string(decoded[2:])
        )

        line = line[next_space:].lstrip(' ')
        for game_result in game_results:
            if line.startswith(game_result):
                human_readable += [game_result]
                return human_readable
        if gp.game_result() is not None:
            raise DecodeError("Expected end of game")

        next_space = end_word(line)
        black_turn = line[:next_space]
        try:
            decoded = decode_move(black_turn, gp.board, BLACK)
        except:
            raise DecodeError("Expected correct move description: `{0}`".format(black_turn))
        human_readable += [decoded]
        gp.make_turn(
            Coordinates.from_string(decoded[:2]),
            Coordinates.from_string(decoded[2:])
        )
        line = line[next_space:].lstrip(' ')

        n += 1

    raise DecodeError("Expected game result")
