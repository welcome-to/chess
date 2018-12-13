from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove

from common_operations import another_color, create_move
from castling_moves import *
from e_p_moves import *
from fucking_cord_const import *
from common_moves import *

from copy import deepcopy
from itertools import filterfalse

import sys

__all__ = ["game_status", "possible_moves", "is_kamikadze", "create_move", "commit_move"]


def possible_moves(board, player_color, previous_move, kamikadze_allowed=False):
    figures = figures_on_board(board, color=player_color)
    all_moves = sum(
        [(possible_moves_from_position(board, start[1], player_color, previous_move)) for start in figures],
        []
    )
    if not kamikadze_allowed:
        all_moves = list(filterfalse(
            lambda turn: is_kamikadze(board, turn, previous_move),
            all_moves
        ))

    return all_moves


def possible_moves_from_position(board, position, player_color, previous_move):
    result = []
    #FIXME: not end points but moevs should be returned
    result.extend(possible_common_moves_from_position(board, position, player_color))
    result.extend(possible_e_p_from_position(board, position, player_color, previous_move))
    result.extend(posible_castling_from_position(board, position, player_color))
    return(result)


# has the game finished with a result? return this result if yes
# current_player: the one whose turn is next
def game_status(board, current_player, previous_turn):
    # are there possible moves for `current_player'?
    all_moves = possible_moves(board, current_player, previous_turn, kamikadze_allowed=False)
    if all_moves: # there are moves, so the game is not over
        return None

    enemy_color = another_color(current_player)
    king_position = figures_on_board(board, type=KING, color=current_player)[0][1]

    enemy_moves = possible_moves(board, enemy_color, None, kamikadze_allowed=True)
    if list(filter(lambda move: move.end == king_position, enemy_moves)): # king can be eaten. checkmate
        print("It's checkmate.", file=sys.stderr)
        if current_player == WHITE:
            return BLACK_WIN
        return WHITE_WIN

    # king is safe. stalemate
    print("It's stalemate.", file=sys.stderr)
    return TIE


def is_kamikadze(board, move, previous_move):
    figure = board.figure_on_position(move.start)
    player_color = figure.color
    back_move = commit_move(move, board, previous_move, player_color)
    king_pos = figures_on_board(board, type=KING, color=player_color)[0][1]
    enemy_color = another_color(player_color)
    if king_pos in fields_under_attack(board, enemy_color):
        commit_move(back_move, board, previous_move, player_color)
        return True

    commit_move(back_move, board, previous_move, player_color)
    return False


def commit_move(move, board, prev_move, player_color):
    if move.is_back_move:
        board.move(move.start, move.end)
        if move.lost_virginity:
            board.figure_on_position(move.end).has_moved = False
        if move.restored_figure is not None:
            board.put(move.eaten_position, move.restored_figure)
        if move.extra_move is not None:
            board.move(move.extra_move.start, move.extra_move.end)
            board.figure_on_position(move.end).has_moved = False
            board.figure_on_position(move.extra_move.end).has_moved = False

    elif move.type == CASTLING_MOVE:
        if is_castling_correct(move, board, player_color):
            board.move(move.start, move.end)
            board.move(move.extra_move.start, move.extra_move.end)

            return Move(
                move.end,
                move.start,
                is_back_move=True,
                extra_move=Move(move.extra_move.end, move.extra_move.start)
            )

        raise InvalidMove("Incorrect castling")

    else:
        lost_virginity = not board.figure_on_position(move.start).has_moved
        if move.type == E_P_MOVE:
            if prev_move is None or not is_e_p_correct(board, move.start, move.end, prev_move, player_color):
                raise InvalidMove("Incorrect e.p.")

            eaten_figure = board.figure_on_position(move.eaten_position)

            board.move(move.start, move.end)
            board.pop(move.eaten_position)

        elif move.type == COMMON_MOVE:
            eaten_figure = board.figure_on_position(move.end)
            if move.end not in possible_common_moves_from_position(board, move.start, player_color):
                raise InvalidMove("Incorrect move: {0}".format(move))
            else:
                board.move(move.start, move.end)
            if move.after_conversion != None:
                board.put(move.end,move.after_conversion)

        else:
            raise InternalError("Wrong move type. This couldn't happen")
        return Move(
            move.end,
            move.start,
            is_back_move=True,
            eaten_position=move.eaten_position,
            restored_figure=eaten_figure,
            lost_virginity=lost_virginity,
            after_conversion=move.after_conversion
        )

