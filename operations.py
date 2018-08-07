from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError

from copy import deepcopy
from itertools import filterfalse


# has the game finished with a result? return this result if yes
# current_player: the one whose turn is next
def game_status(board, current_player):
    # are there possible moves for `current_player'?
    all_moves = list(filterfalse(
        lambda item: IsKamikadze(board, item[0])(item[1]),
        possible_moves(board, current_player, None)
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
        print("It's checkmate.")
        if current_player == WHITE:
            return BLACK_WIN
        return WHITE_WIN

    # king is safe. stalemate
    print("It's stalemate.")
    return TIE


# is the `turn' correct at this position?
def is_correct(turn, board, player_color):
    print("Player {0}. Turn: {1} -> {2}".format(player_color, turn.start, turn.end))
    if str(turn.start)+str(turn.end) in CASTLING_TYPES:
        turn.is_roque = True
        CastlingType = str(turn.start)+str(turn.end)
    if turn.is_roque:
        # 1. Check there are no extra figures.
        # 2. Check the figures haven't moved.
        if CastlingType == 'e1g1':
            if (not (board.figure_on_position(Coordinates.from_string('f1')) is None)) or (not (board.figure_on_position(Coordinates.from_string('g1')) is None)):
                return False
            if board.figure_on_position(turn.start).has_moved or board.figure_on_position(Coordinates.from_string('h1')):
                return False
        if CastlingType == 'e8g8':
            if (not (board.figure_on_position(Coordinates.from_string('f8')) is None)) or (not (board.figure_on_position(Coordinates.from_string('g8')) is None)):
                return False
            if board.figure_on_position(turn.start).has_moved or board.figure_on_position(Coordinates.from_string('h8')):
                return False
        if CastlingType == 'e1c1':
            if (not (board.figure_on_position(Coordinates.from_string('d1')) is None)) or (not (board.figure_on_position(Coordinates.from_string('c1')) is None)) or (not (board.figure_on_position(Coordinates.from_string('b1')) is None)):
                return False
            if board.figure_on_position(turn.start).has_moved or board.figure_on_position(Coordinates.from_string('a1')):
                return False
        if CastlingType == 'e8c8':
            if (not (board.figure_on_position(Coordinates.from_string('d8')) is None)) or (not (board.figure_on_position(Coordinates.from_string('c8')) is None)) or (not (board.figure_on_position(Coordinates.from_string('b8')) is None)):
                return False
            if board.figure_on_position(turn.start).has_moved or board.figure_on_position(Coordinates.from_string('a8')):
                return False
        # 2. Check the figures haven't moved.
        # 3. Check the king's way is not under attack.
        is_kamikadze = IsKamikadze(board,turn.start)
        #if is_kamikadze(turn.end):
            #print('Kamikadze')
            #return False
        return True

    figure = board.figure_on_position(turn.start)
    if ((figure is None) or (figure.color != player_color)):
        return False
    listofmoves = possible_moves_from_position(board,turn.start,player_color,None) # FIXME: wtf None
    is_kamikadze = IsKamikadze(board,turn.start)
    moves = filterfalse(is_kamikadze, listofmoves)

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
    rook_move = CASTLING_TYPES[str(king_move)]
    rook_move = Move(*map(Coordinates.from_string, [rook_move[:2], rook_move[2:]]))
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


class IsKamikadze(object):
    def __init__(self, board, initial_position):
        figure_color = board.figure_on_position(initial_position).color
        self.board = deepcopy(board)
        if figure_color == BLACK:
            self.enemy_color = WHITE
        else:
            self.enemy_color = BLACK
        self.figure_set = figures_on_board(board, color=self.enemy_color)
        self.king_pos = figures_on_board(board, type=KING, color=figure_color)[0][1]
        self.figure = board.figure_on_position(initial_position)
        self.board.pop(initial_position)

    def __call__(self,final_position):
        self.board.put(final_position,self.figure)
        for i in self.figure_set:
            if self.king_pos in possible_moves_from_position(self.board,i[1],self.enemy_color,None):
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
