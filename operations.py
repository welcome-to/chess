from board import Figure, Move, Coordinates
from const import *
from exception import InternalError


# has the game finished with a result? return this result if yes
def game_status(board, current_player):
    return None


# is the `turn' correct at this position?
def is_correct(turn, board, player_color):
    if turn.is_roque:
        return True

    figure = board.figure_on_position(turn.start)
    if ((figure is None) or (figure.color != player_color)):
        return False
    listofmoves = possible_moves(board,turn.start,player_color,None)
    if not turn.end in listofmoves:
        return False
    return True


def convert_pawns(board):
    for i in range(8):
        figure = board.figure_on_position(Coordinates(i, 7))
        if figure is not None and figure.type == PAWN: # it can be only white
            board.put(Coordinates(i,7), Figure(WHITE, QUEEN))

        figure = board.figure_on_position(Coordinates(i, 0))
        if figure is not None and figure.type == PAWN:
            board.put(Coordinates(i,0),Figure(BLACK, QUEEN))


def make_castling(board, king_move):
    rook_move = Move(castling_types[str(king_move)])
    try:
        board.move(rook_move.start, rook_move.end)
        board.move(king_move.start, king_move.end)
    except:
        raise InternalError("Castling suddenly failed")


# this is a class-functor. it can be used as a function: instance(arg) === __call__(self, arg).
class NotBeatingSameColor(object):
    def __init__(self, board, initial_position):
        figurecolor = board.figure_on_position(initial_position).color
        if figurecolor == WHITE:
            figureset = board.white_figures()
        else:
            figureset = board.black_figures()
        self.positionset = []
        for i in figureset:
            self.positionset.append(i[1])

    def __call__(self, final_position):
        if not (final_position in self.positionset):
            return True
        else:
            return False


class NotCrossingOccupiedField(object):
    def __init__(self,board,initial_position):
        pass
    def __call__(self,final_position):
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
    given_args = {
        PAWN: [position,board],
        ROOK: [position,board],
        KNIGHT: [position],
        BISHOP: [position,board],
        QUEEN: [position,board],
        KING: [position]
    }
    not_beating_same_color = NotBeatingSameColor(board, position)
    not_crossing_occupied_field = NotCrossingOccupiedField(board, position)

    moves = type_to_handler[figure.type](*given_args[figure.type])
    moves = filter(not_beating_same_color, moves)
    moves = filter(not_crossing_occupied_field, moves)
    return moves


class TryEat(object):
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def __call__(self, position):
        figure = self.board.figure_on_position(position)
        if figure is not None and figure.color != self.color:
            return position


def raw_possible_moves_pawn(position, board):
    pawn = board.figure_on_position(position)
    full = []
    try_eat = TryEat(board, pawn.color)
    if pawn.color == BLACK:
        if position.bottom() and board.figure_on_position(position.bottom()) is None:
            full.append(position.bottom())
            if not pawn.has_moved and board.figure_on_position(position.bottom().bottom()) is None:
                full.append(position.bottom().bottom())
        full += list(filter(
            lambda x: x is not None,
            map(try_eat, [position.bottom_left(), position.bottom_right()])
        ))
    else:
        if position.top() and board.figure_on_position(position.top()) is None:
            full.append(position.top())
            if not pawn.has_moved and board.figure_on_position(position.top().top()) is None:
                full.append(position.top().top())
        full += list(filter(
            lambda x: x is not None,
            map(try_eat, [position.top_left(), position.top_right()])
        ))
    return full


def raw_possible_moves_king(position):
    return list(filter(
        bool,
        [position.left(), position.right(), position.top(), position.bottom(),
         position.top_left(), position.top_right(), position.bottom_left(), position.bottom_right()]
    ))


def raw_possible_moves_rook(position,board):
    full = []
    coord = position.right()
    while coord:
        full.append(coord)
        coord = coord.right()
    coord = position.left()
    while coord:
        full.append(coord)
        coord = coord.left()
    coord = position.top()
    while coord:
        full.append(coord)
        coord = coord.top()
    coord = position.bottom()
    while coord:
        full.append(coord)
        coord = coord.bottom()
    return full


def raw_possible_moves_knight(position):
    return list(filter(
        bool,
        [position.top().top_right(),position.top().top_left(),position.bottom().bottom_right(),position.bottom().bottom_left(),
         position.left().top_left(),position.left().bottom_left(),position.right().top_right(),position.right().bottom_right()]
    ))


def raw_possible_moves_bishop(position,board):
    full = []
    coord = position.top_right()
    while coord:
        full.append(coord)
        coord = coord.top_right()
    coord = position.bottom_right()
    while coord:
        full.append(coord)
        coord = coord.bottom_right()
    coord = position.top_left()
    while coord:
        full.append(coord)
        coord = coord.top_left()
    coord = position.bottom_left()
    while coord:
        full.append(coord)
        coord = coord.bottom_left()
    return full


def raw_possible_moves_queen(position,board):
    return raw_possible_moves_rook(position,board) + raw_possible_moves_bishop(position,board)
    return full
