from const import *


class TryEat(object):
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def __call__(self, position):
        if position:
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
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.right()
    coord = position.left()
    while coord:
        full.append(coord)
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.left()
    coord = position.top()
    while coord:
        full.append(coord)
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.top()
    coord = position.bottom()
    while coord:
        full.append(coord)
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.bottom()
    return full


def raw_possible_moves_knight(position):
    return list(filter(
        bool,
        [position.top().top_right(),position.top().top_left(),
         position.bottom().bottom_right(),position.bottom().bottom_left(),
         position.left().top_left(),position.left().bottom_left(),
         position.right().top_right(),position.right().bottom_right()]
    ))


def raw_possible_moves_bishop(position,board):
    full = []
    coord = position.top_right()
    while coord:
        full.append(coord)
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.top_right()
    coord = position.bottom_right()
    while coord:
        full.append(coord)
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.bottom_right()
    coord = position.top_left()
    while coord:
        full.append(coord)
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.top_left()
    coord = position.bottom_left()
    while coord:
        full.append(coord)
        if board.figure_on_position(coord) is not None:
            break
        coord = coord.bottom_left()
    return full


def raw_possible_moves_queen(position,board):
    return raw_possible_moves_rook(position,board) + raw_possible_moves_bishop(position,board)
