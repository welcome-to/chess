from board import Board, Coordinates, Move, figures_on_board
from const import *
from common_operations import is_e_p, create_move
from operations import possible_moves_from_position
from game_engine import GameProcessor

import copy
import sys
import re


class DecodeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class MoveInfo(object):
    def __init__(self, is_check=False, is_checkmate=False, is_idiotic=False, convert_to=None):
        self.is_check = is_check
        self.is_checkmate = is_checkmate
        self.is_idiotic = is_idiotic
        self.convert_to = convert_to


def decode_move(short_line, board, player_color, previous_move):
    def extract_comment(short_line):
        move_info = MoveInfo()
        if short_line[-1] == '#':
            move_info.is_checkmate = True
            short_line = short_line[:-1]
        elif short_line[-1] == '+':
            move_info.is_check = True
            short_line = short_line[:-1]
        # let's consider all graded moves the same way (FIXME if it stops being isopenisual)
        elif short_line.endswith('??') or short_line.endswith('!!') or short_line.endswith('!?') or short_line.endswith('?!'):
            move_info.is_idiotic = True
            short_line = short_line[:-2]
        elif short_line.endswith('?') or short_line.endswith('!'):
            move_info.is_idiotic = True
            short_line = short_line[:-1]
        return short_line, move_info

    move_info = MoveInfo()
    if short_line.startswith('0-0-0'):
        # FIXME: there could be a length assertion here
        if len(short_line) > 5:
            short_line, move_info = extract_comment(short_line[5:])
        return ('e1c1', move_info) if player_color == WHITE else ('e8c8', move_info)

    if short_line.startswith('0-0'):
        if len(short_line) > 3:
            short_line, move_info = extract_comment(short_line[3:])
        return ('e1g1', move_info) if player_color == WHITE else ('e8g8', move_info)

    # FIXME: add checks that +, #, x are correct: really suspense, or gameover, or figure eaten
    # and exceptions
    short_line, move_info = extract_comment(short_line)

    LETTER_TO_FIGURE_TYPE = {'p': PAWN, 'K': KING, 'Q': QUEEN, 'N': KNIGHT, 'B': BISHOP, 'R': ROOK}

    is_conversion = False
    if short_line[-1] in ['Q', 'R', 'N', 'B']: # FIXMEEEEE (gp)
        is_conversion = True
        move_info.convert_to = LETTER_TO_FIGURE_TYPE[short_line[-1]]
        short_line = short_line[:-1]
    # FIXME: check that it's really pawn move to the last horizontal

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
        figure_type = LETTER_TO_FIGURE_TYPE[short_line[-1]]

    candidates = figures_on_board(board, type=figure_type, color=player_color)
    if initial_x:
        candidates = list(filter(lambda item: item[1].x == LETTER_TO_INDEX[initial_x], candidates))
    elif initial_y:
        candidates = list(filter(lambda item: item[1].y == int(initial_y) - 1, candidates))

    final_pos = Coordinates.from_string(end_field)
    candidates = list(filter(
        lambda item: final_pos in map(lambda move: move.end, possible_moves_from_position(board, item[1], player_color, previous_move)),
        candidates
    ))

    if not candidates:
        raise DecodeError("No suitable figures for turn")
    if len(candidates) > 1:
        raise DecodeError("Too many suitable figures for turn")
    if figure_type != candidates[0][0].type:
        raise DecodeError("Wrong figure type: declared {0}, found {1}".format(figure_type, candidates[0][0].type))
    if player_color != candidates[0][0].color:
        raise DecodeError("Found figure of color {0} but it's {1} turn".format(candidates[0][0].color, player_color))

    start_pos = candidates[0][1]
    if is_eating:
        attacked_field = final_pos
        if is_e_p(start_pos, final_pos, board):
            attacked_field = Coordinates(final_pos.x, start_pos.y)
        eaten_figure = board.figure_on_position(attacked_field)
        if eaten_figure is None:
            raise DecodeError("Expected eating at {0} but there's no figure to eat".format(attacked_field))
        if eaten_figure.color == player_color:
            raise DecodeError("Expected figure of another color at {0}".format(attacked_field))

    return (str(start_pos) + end_field), move_info


GAME_RESULTS = ['1-0', '0-1', '1/2']


class Decoder(object):
    def __init__(self, raise_if_incomplete=True):
        self.raise_if_incomplete = raise_if_incomplete
        self._reset()

    def __call__(self, line):
        self._reset()
        line = re.sub('\[.*?\]', '', line)

        while line:
            line = self._call_once(line)

        if not self.game_over and self.raise_if_incomplete: # there was no game result at the end of the line
            raise DecodeError("Expected game result")

        self.human_readable_game += line
        return self.human_readable_game

    def _reset(self):
        self.gp = GameProcessor()
        self.previous_move = None
        self.move_number = 1
        self.human_readable_game = []
        self.game_over = False

    def _player_color(self):
        if self.move_number % 2 == 1:
            return WHITE
        return BLACK

    def _call_once(self, line):
        def _end_word(line):
            result = line.find(' ')
            if result == -1:
                return len(line)
            return result

        turn_number = self.move_number // 2 + 1
        if self._player_color() == WHITE:
            print("Turn #{0}".format(turn_number), file=sys.stderr)

        line = line.lstrip(' ')
        for game_result in GAME_RESULTS:
            if line.startswith(game_result):
                self.human_readable_game += [game_result]
                self.game_over = True
                return '' #FIXME

        if self.gp.is_game_over():
            raise DecodeError("Expected end of game")

        if self._player_color() == WHITE:
            prefix = str(turn_number) + '.'
            if not line.startswith(prefix):
                raise DecodeError("Expected turn number: {0} in '{1}'".format(turn_number, line))
            line = line[len(prefix):]

        next_space = _end_word(line)
        first_word = line[:next_space]
        line = line[next_space:].lstrip(' ')
        if not first_word:
            if self.raise_if_incomplete:
                raise DecodeError("Expected game result")
            return line
        try:
            # FIXME: check move_info
            decoded, move_info = decode_move(first_word, self.gp.board, self._player_color(), self.previous_move)
        except:
            raise
        self.human_readable_game += [decoded]
        start, end = map(Coordinates.from_string, (decoded[:2], decoded[2:]))
        self.previous_move = create_move(start, end, self.gp.board, self.gp.current_player, figure_to_create=move_info.convert_to)
        self.gp.make_move(start, end, figure_to_create=move_info.convert_to)

        self.move_number += 1
        return line


def decode_game(line, raise_if_incomplete=True):
    decode = Decoder(raise_if_incomplete)
    return decode(line)
