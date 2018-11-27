from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove


from common_operations import NotBeatingSameColor,another_color
from castling_moves import *
from e_p_moves import *
from possible_moves import *
from fucking_cord_const import *
from common_moves import *

from copy import deepcopy
from itertools import filterfalse

import sys
'''
Хуйня!!! Пофиксить.. Не использовать create_move
'''
def posible_castling_from_position(board,position,current_player):
    figure = board.figure_on_position(position)
    if current_player == BLACK:
        move1 = create_move(position, Coordinates.from_string('G8'), board, current_player)
        move2 = create_move(position, Coordinates.from_string('C8'), board, current_player)
    else:
        move1 = create_move(position, Coordinates.from_string('G1'), board, current_player)
        move2 = create_move(position, Coordinates.from_string('C1'), board, current_player)
    ans = []
    try:
        if move1.type == CASTLING_MOVE:
            if is_castling_correct(move1, board, current_player):
                ans.append(move1)
    except:
        pass
    try:
        if move2.type == CASTLING_MOVE:
            if is_castling_correct(move2, board,current_player):
                ans.append(move2)
    except:
        pass
    return ans

def possible_moves(board, player_color, previous_move):
    figures = figures_on_board(board, color=player_color)
    return sum(
        [(possible_moves_from_position(board, start[1], player_color, previous_move)) for start in figures],
        []
    )






def possible_moves_from_position(board, position, player_color, previous_move):
    result = []
    #FIXME: not end points but moevs should be returned

    for item in possible_common_moves_from_position(board, position, player_color):
        result.append(create_move(position, item, board, player_color))
    for turn in possible_e_p_from_position(board, position, player_color, previous_move):
        result.append(create_move(position, turn, board, player_color))
    result.extend(posible_castling_from_position(board, position, player_color))
    return(result)





# has the game finished with a result? return this result if yes
# current_player: the one whose turn is next
def game_status(board, current_player, previous_turn):
    # are there possible moves for `current_player'?
    all_moves = allowed_moves(board,current_player,previous_turn)
    if all_moves: # there are moves, so the game is not over
        return None

    enemy_color = another_color(current_player)
    king_position = figures_on_board(board, type=KING, color=current_player)[0][1]

    enemy_moves = possible_moves(board, enemy_color, None)
    if list(filter(lambda move: move.end == king_position, enemy_moves)): # king can be eaten. checkmate
        print("It's checkmate.", file=sys.stderr)
        if current_player == WHITE:
            return BLACK_WIN
        return WHITE_WIN

    # king is safe. stalemate
    print("It's stalemate.", file=sys.stderr)
    return TIE






def allowed_moves_from_position(board, position, player_color, previous_turn):
    list_of_moves = possible_moves_from_position(board, position, player_color, previous_turn)
    return list(filterfalse(
        lambda move: is_kamikadze(board, move, previous_turn),
        list_of_moves
    ))


def allowed_moves(board, current_player, previous_turn):
    # FIXME: this won't work.
    all_moves = list(filterfalse(
        lambda turn: is_kamikadze(board, turn, previous_turn),
        possible_moves(board, current_player, previous_turn)
    ))
    return all_moves


def convert_pawns(board):
    for i in range(8):
        figure = board.figure_on_position(Coordinates(i, 7))
        if figure is not None and figure.type == PAWN: # it can be only white
            board.put(Coordinates(i,7), Figure(WHITE, QUEEN))

        figure = board.figure_on_position(Coordinates(i, 0))
        if figure is not None and figure.type == PAWN:
            board.put(Coordinates(i,0),Figure(BLACK, QUEEN))




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







def create_move(start, end, board, player_color):
    figure = board.figure_on_position(start)
    if figure is None or figure.color != player_color:
        raise InvalidMove("No valid figure at {0}".format(start))
    if is_castling(start, end, board):
        print(start,type(end))
        rook_move = CASTLING_DATA[(start, end)]['rook_move']
        extra_move = Move(*rook_move)
        return Move(start, end, type=CASTLING_MOVE, extra_move=extra_move)

    eaten_position = Coordinates(end.x, start.y)
    if is_e_p(start, end, board):
        return Move(start, end, type=E_P_MOVE, eaten_position=eaten_position)

    if board.figure_on_position(end) is not None:
        eaten_position = end
    else:
        eaten_position = None
    return Move(start, end, type=COMMON_MOVE, eaten_position=eaten_position)


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
                raise InvalidMove("Incorrect move")
            else:
                board.move(move.start, move.end)

        else:
            raise InternalError("Wrong move type. This couldn't happen")
        return Move(
            move.end,
            move.start,
            is_back_move=True,
            eaten_position=move.eaten_position,
            restored_figure=eaten_figure,
            lost_virginity=lost_virginity
        )

