from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove

from possible_moves import *

from copy import deepcopy
from functools import reduce
from itertools import filterfalse

import sys


# has the game finished with a result? return this result if yes
# current_player: the one whose turn is next
def game_status(board, current_player, previous_turn):
    # are there possible moves for `current_player'?
    all_moves = list(filterfalse(
        lambda turn: is_kamikadze(board, turn, previous_turn),
        possible_moves(board, current_player, previous_turn)
    ))
    if all_moves: # there are moves, so the game is not over
        return None

    enemy_color = another_color(current_player)
    king_position = figures_on_board(board, type=KING, color=current_player)[0][1]

    enemy_moves = possible_moves(board, enemy_color, None)
    if list(filter(lambda item: item.end == king_position, enemy_moves)): # king can be eaten. checkmate
        print("It's checkmate.", file=sys.stderr)
        if current_player == WHITE:
            return BLACK_WIN
        return WHITE_WIN

    # king is safe. stalemate
    print("It's stalemate.", file=sys.stderr)
    return TIE


def is_pawn_moved(board,move):
    figure = board.figure_on_position(move.end)
    if figure is not None and figure.type == PAWN:
        return True
    return False


def another_color(color):
    return WHITE if color == BLACK else BLACK


def is_castling(start, end, board):
    figure = board.figure_on_position(start)
    if figure is None or figure.type is not KING:
        return False
    return (str(start) + str(end)) in CASTLING_DATA.keys()


def is_castling_correct(king_move, board, player_color):
    assert(king_move.type == CASTLING_MOVE)

    castling_data = CASTLING_DATA[str(king_move)]
    rook_move = king_move.extra_move

    king = board.figure_on_position(king_move.start)
    if king.color != player_color or king.color != CASTLING_DATA[str(king_move)]['color']:
        return False

    rook = board.figure_on_position(rook_move.start)
    if rook is None or rook.color != player_color or rook.color != CASTLING_DATA[str(king_move)]['color']:
        return False

    if king.has_moved or rook.has_moved:
        return False

    # no figures between king and rook
    for inner_field in castling_data['inner_fields']:
        if not board.figure_on_position(Coordinates.from_string(inner_field)) is None:
            return False

    # 3. Check the king's way is not under attack.
    under_attack = fields_under_attack(board, another_color(player_color))
    if set(map(Coordinates.from_string, castling_data['safe_fields'])) & set(under_attack):
        return False

    return True


def allowed_moves_from_position(board, position, player_color, previous_turn):
    list_of_moves = possible_moves_from_position(board, position, player_color, previous_turn)
    return list(filterfalse(
        lambda move: is_kamikadze(board, move, previous_turn),
        list_of_moves
    ))


def allowed_moves(board, previous_turn):
    # FIXME: this won't work.
    figures = figures_on_board(board, color=player_color)
    return sum(
        [(allowed_moves_from_position(board, start[1], player_color, previous_move)) for start in figures],
        []
    )


def convert_pawns(board):
    for i in range(8):
        figure = board.figure_on_position(Coordinates(i, 7))
        if figure is not None and figure.type == PAWN: # it can be only white
            board.put(Coordinates(i,7), Figure(WHITE, QUEEN))

        figure = board.figure_on_position(Coordinates(i, 0))
        if figure is not None and figure.type == PAWN:
            board.put(Coordinates(i,0),Figure(BLACK, QUEEN))


def make_castling(board, king_move):
    rook_move = Move.from_string(CASTLING_DATA[str(king_move)]['rook_move'])
    try:
        board.move(rook_move.start, rook_move.end)
        board.move(king_move.start, king_move.end)
    except:
        raise InternalError("Castling suddenly failed")


# this is a class-functor. it can be used as a function: instance(arg) === __call__(self, arg).
class NotBeatingSameColor(object):
    def __init__(self, board, initial_position):
        figure_color = board.figure_on_position(initial_position).color
        figure_set = figures_on_board(board, color=figure_color)
        self.position_set = []
        for i in figure_set:
            self.position_set.append(i[1])

    def __call__(self, final_position):
        if not (final_position in self.position_set):
            return True
        else:
            return False

# FIXME: fields_under_attack
def fields_under_attack(board, enemy_color):
    attacked = [possible_common_moves_from_position(board, item[1], enemy_color) for item in figures_on_board(board, color=enemy_color)]
    # FIXME: e_p_moves
    return reduce(lambda x,y: set(x) | set(y), attacked, set())


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


def possible_moves(board, player_color, previous_move):
    figures = figures_on_board(board, color=player_color)
    return sum(
        [(possible_moves_from_position(board, start[1], player_color, previous_move)) for start in figures],
        []
    )


def possible_moves_from_position(board, position, player_color, previous_move):
    result = []
    for item in possible_common_moves_from_position(board, position, player_color):
        if board.figure_on_position(item) is not None:
            eaten_position = item
        else:
            eaten_position = None
        result.append(Move(position, item, type=COMMON_MOVE,eaten_position = eaten_position))
    for turn in possible_e_p_from_position(board, position, player_color, previous_move):
        result.append(Move(position, turn, type=E_P_MOVE, eaten_position=Coordinates(position.x, item.y)))
    return(result)


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

def possible_e_p_from_position(board, position, player_color, previous_move):
    if not previous_move or not position.x in [1, 6] or not is_pawn_jump(board, previous_move, another_color(player_color)):
        return []

    return filter(
        lambda end: is_e_p_correct(board, position, end, previous_move, player_color),
        filter(bool, [
            position.top_left(), position.top_right(),
            position.bottom_left(), position.bottom_right()
        ])
    )

def is_e_p(start, end, board):
    figure = board.figure_on_position(start)
    if not figure.type == PAWN:
        return False
    if start.x == end.x:
        return False
    return board.figure_on_position(end) is None


def is_e_p_correct(board, start, end, prev_move, player_color):
    if not is_pawn_jump(board, prev_move, another_color(player_color)):
        return False
    if abs(prev_move.start.x - start.x) != 1 or \
       prev_move.start.y - end.y != end.y - prev_move.end.y or \
       abs(prev_move.start.y - end.y) != 1:
       return False
    return True


def is_pawn_jump(board, move, color):
    figure = board.figure_on_position(move.end)
    if figure is None or figure.color != color:
        raise InternalError("This could not happen")
    if figure.type != PAWN:
        return False

    return (color == WHITE and move.end.y - move.start.y == 2) or (color == BLACK and move.end.y - move.start.y == -2)


def create_move(start, end, board, player_color):
    figure = board.figure_on_position(start)
    if figure is None or figure.color != player_color:
        raise InvalidMove("No valid figure at {0}".format(start))
    if is_castling(start, end, board):
        king_move = str(start) + str(end)

        rook_move = CASTLING_DATA[king_move]['rook_move']
        extra_move = Move(*map(Coordinates.from_string, rook_move))
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
