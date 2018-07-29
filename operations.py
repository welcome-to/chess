from board import Figure, Move
from const import *
from exception import InternalError


# has the game finished with a result? return this result if yes
def game_status(board, current_player):
    return None


# is the `turn' correct at this position?
def is_correct(turn, board, player_color):
    if turn.is_roque:
        return True

    figure = board.figure_on_position(turn.start.x, turn.start.y)
    if figure is None or figure.color != player_color:
        return False

    return True


def convert_pawns(board):
    for i in range(8):
        figure = board.figure_on_position(i, 7)
        if figure is not None and figure.type == PAWN: # it can be only white
            board.data[7][i] = Figure(WHITE, QUEEN)

        figure = board.figure_on_position(i, 0)
        if figure is not None and figure.type == PAWN:
            board.data[0][i] = Figure(BLACK, QUEEN)


def make_castling(board, king_move):
    castling_types = {'e1g1': 'h1f1', 'e1c1': 'a1d1', 'e8g8': 'h8f8', 'e8c8': 'a8d8'}
    rook_move = Move(castling_types[str(king_move)])
    try:
        board.move(rook_move.start, rook_move.end)
        board.move(king_move.start, king_move.end)
    except:
        raise InternalError("Castling suddenly failed")


# this is a class-functor. it can be used as a function: instance(arg) === __call__(self, arg).
class NotBeatingSameColor(object):
    def __init__(self, board, initial_position):
        pass

    def __call__(self, final_position):
        return True


def possible_moves(board, position, player_color, previous_move):
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
    not_beating_same_color = NotBeatingSameColor(board, position)
    not_crossing_occupied_field = NotCrossingOccupiesField(board, position)

    moves = type_to_handler[figure.type](position)
    moves = filter(not_beating_same_color, moves)
    moves = filter(not_crossing_occupied_field, moves)
    return moves


def raw_possible_moves_king(position):
    x,y = position.x, position.y
    full = [(x-1, y-1), (x, y-1), (x+1, y-1)] # ...
