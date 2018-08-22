from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError

from copy import deepcopy
from functools import reduce
from itertools import filterfalse

import sys


# has the game finished with a result? return this result if yes
# current_player: the one whose turn is next
def game_status(board, current_player, previous_turn):
    # are there possible moves for `current_player'?
    all_moves = list(filterfalse(
        lambda item: IsKamikadze(board, item[0])(item[1]),
        possible_moves(board, current_player, previous_turn)
    ))
    if all_moves: # there are moves, so the game is not over
        return None

    if current_player == WHITE:
        enemy_color = BLACK
    else:
        enemy_color = WHITE
    king_position = figures_on_board(board, type=KING, color=current_player)[0][1]

    enemy_moves = possible_moves(board, enemy_color, None)
    if list(filter(lambda item: item[1] == king_position, enemy_moves)): # king can be eaten. checkmate
        print("It's checkmate.", file=sys.stderr)
        if current_player == WHITE:
            return BLACK_WIN
        return WHITE_WIN

    # king is safe. stalemate
    print("It's stalemate.", file=sys.stderr)
    return TIE


def another_color(color):
    return WHITE if color == BLACK else BLACK


def is_castling(move, board):
    figure = board.figure_on_position(move.start)
    if figure is None or figure.type is not KING:
        return False
    return str(move) in CASTLING_DATA.keys()


def is_castling_correct(king_move, board, player_color):
    castling_data = CASTLING_DATA[str(king_move)]
    rook_move = Move.from_string(castling_data['rook_move'])

    # FIXME: there are excess conditions here
    king = board.figure_on_position(king_move.start)
    if king is None or king.color != player_color or king.color != CASTLING_DATA[str(king_move)]['color']:
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


# is the `turn' correct at this position?
def is_correct(turn, board, player_color, previous_turn):
    print("Player {0}. Turn: {1} -> {2}".format(player_color, turn.start, turn.end), file=sys.stderr)

    if is_castling(turn, board):
        return is_castling_correct(turn, board, player_color)

    figure = board.figure_on_position(turn.start)
    if ((figure is None) or (figure.color != player_color)):
        return False

    list_of_moves = possible_moves_from_position(board, turn.start, player_color, previous_turn)
    is_kamikadze = IsKamikadze(board, turn.start)
    moves = list(filterfalse(is_kamikadze, list_of_moves))

    if not turn.end in moves:
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


def fields_under_attack(board, enemy_color):
    attacked = [possible_moves_from_position(board, item[1], enemy_color, None) for item in figures_on_board(board, color=enemy_color)]
    return reduce(lambda x,y: set(x) | set(y), attacked, set())


class IsKamikadze(object):
    def __init__(self, board, initial_position):
        self.board = deepcopy(board)
        self.figure = board.figure_on_position(initial_position)
        self.enemy_color = another_color(self.figure.color)
        self.figure_set = figures_on_board(self.board, color=self.enemy_color)

        self.board.pop(initial_position)

    def __call__(self,final_position):
        board = deepcopy(self.board)
        board.put(final_position,self.figure)
        king_pos = figures_on_board(board, type=KING, color=self.figure.color)[0][1]
        enemy_color = another_color(self.figure.color)
        figure_set = figures_on_board(board, color=enemy_color)
        for i in figure_set:
            if king_pos in possible_moves_from_position(board,i[1],self.enemy_color,None):
                #print ("Figure in position {0} will eat our beloved James LVII".format(str(i[1])))
                return True
        return False


def possible_moves(board, player_color, previous_move):
    figures = figures_on_board(board, color=player_color)
    return sum(
        map(
            lambda item: [(item[0], boo) for boo in item[1]],
            [(start[1], possible_moves_from_position(board, start[1], player_color, previous_move)) for start in figures]
        ),
        []
    )


def possible_moves_from_position(board, position, player_color, previous_move):
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
        PAWN: [position,board,previous_move],
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


def is_e_p(move, board):
    figure = board.figure_on_position(move.start)
    if not figure.type == PAWN:
        return False
    if move.start.x == move.end.x:
        return False
    return board.figure_on_position(move.end) is None


def make_e_p(board, move):
    board.move(move.start, move.end)
    enemy_pos = Coordinates(move.end.x, move.start.y)
    board.pop(enemy_pos)


def is_pawn_jump(board, move, color):
    figure = board.figure_on_position(move.end)
    if figure is None or figure.color != color:
        raise InternalError("This could not happen")
    if figure.type != PAWN:
        return False

    return (color == WHITE and move.end.y - move.start.y == 2) or (color == BLACK and move.end.y - move.start.y == -2)


class TryEat(object):
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def __call__(self, position):
        if position:
            figure = self.board.figure_on_position(position)
            if figure is not None and figure.color != self.color:
                return position


def raw_possible_moves_pawn(position, board, previous_move):
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

    if previous_move is not None and is_pawn_jump(board, previous_move, another_color(pawn.color)):
        if pawn.color == BLACK:
            full.append(previous_move.end.bottom())
        else:
            full.append(previous_move.end.top())

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
        [position.top().top_right(),position.top().top_left(),position.bottom().bottom_right(),position.bottom().bottom_left(),
         position.left().top_left(),position.left().bottom_left(),position.right().top_right(),position.right().bottom_right()]
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
