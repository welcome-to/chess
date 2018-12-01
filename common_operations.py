from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove
from fucking_cord_const import *






def is_pawn_moved(board,move):
    figure = board.figure_on_position(move.end)
    if figure is not None and figure.type == PAWN:
        return True
    return False


def is_pawn_jump(board, move, color):
    figure = board.figure_on_position(move.end)
    if figure is None or figure.color != color:
        raise InternalError("This could not happen")
    if figure.type != PAWN:
        return False
    return (color == WHITE and move.end.y - move.start.y == 2) or (color == BLACK and move.end.y - move.start.y == -2)


def convert_pawns(board):
    for i in range(8):
        figure = board.figure_on_position(Coordinates(i, 7))
        if figure is not None and figure.type == PAWN: # it can be only white
            board.put(Coordinates(i,7), Figure(WHITE, QUEEN))

        figure = board.figure_on_position(Coordinates(i, 0))
        if figure is not None and figure.type == PAWN:
            board.put(Coordinates(i,0),Figure(BLACK, QUEEN))


def another_color(color):
    return WHITE if color == BLACK else BLACK


def is_castling(start, end, board):
    figure = board.figure_on_position(start)
    if figure is None or figure.type is not KING:
        return False
    return (start,end) in CASTLING_DATA.keys()


def is_e_p(start, end, board):
    figure = board.figure_on_position(start)
    if not figure.type == PAWN:
        return False
    if start.x == end.x:
        return False
    return board.figure_on_position(end) is None


def create_move(start, end, board, player_color):
    figure = board.figure_on_position(start)
    if figure is None or figure.color != player_color:
        raise InvalidMove("No valid figure at {0}".format(start))
    if is_castling(start, end, board):
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
