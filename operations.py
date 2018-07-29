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


def possible_moves(figure, board, previous_move):
    type_to_handler = {
        PAWN: possible_moves_pawn,
        ROOK: possible_moves_rook,
        KNIGHT: possible_moves_knight,
        BISHOP: possible_moves_bishop,
        QUEEN: possible_moves_queen,
        KING: possible_moves_king
    }
    return type_to_handler[figure.type](figure, board, previous_move)
