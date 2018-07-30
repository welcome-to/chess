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

    figure = board.figure_on_position(turn.start.x, turn.start.y)
    if ((figure is None) or (figure.color != player_color)):
        return False
    listofmoves = possible_moves(board,turn.start,player_color,None)
    if not (turn.end in listofmoves):
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
    rook_move = Move(castling_types[str(king_move)])
    try:
        board.move(rook_move.start, rook_move.end)
        board.move(king_move.start, king_move.end)
    except:
        raise InternalError("Castling suddenly failed")


# this is a class-functor. it can be used as a function: instance(arg) === __call__(self, arg).
class NotBeatingSameColor(object):
    def __init__(self, board, initial_position):
        figurecolor = board.figure_on_position(initial_position.x,initial_position.y).color
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
class NotCrossingOccupiesField(object):
    def __init__(self,board,initial_position):
        pass
    def __call__(self,final_position):
        return True
        


def possible_moves(board, position, player_color, previous_move):
    figure = board.figure_on_position(position.x,position.y)
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

    moves = cordfromlist(type_to_handler[figure.type](position))
    moves = filter(not_beating_same_color, moves)
    moves = filter(not_crossing_occupied_field, moves)
    return moves

def cordfromlist(listofcord):
    for i in range(len(listofcord)):
        print(list[i])
        cord = Coordinates(list[i][0],list[i][0])
        list[i] = cord


def raw_possible_moves_pawn(position):
    pass

def raw_possible_moves_king(position):
    return list(filter(
        lambda x: x is not None,
        [position.left(), position.right(), position.top(), position.bottom(),
         position.top_left(), position.top_right(), position.bottom_left(), position.bottom_right()]
    ))

def raw_possible_moves_rook(position):
    x,y = position.x,position.y
    full = []
    byx = x
    while byx < 7:
        byx +=1
        full.append((byx,y))
    byx = x
    while byx > 0:
        byx -= 1
        full.append((byx,y))
    byy = y
    while byy < 7:
        byy +=1
        full.append((x,byy))
    byy = y
    while byy > 0:
        byy -= 1
        full.append((x,byy))
    return full
def raw_possible_moves_knight(position):
    x,y = position.x, position.y
    full = [(x+2,y+1),(x+2,y-1),(x-2,y+1),(x-2,y-1),(x+1,y+2),(x+1,y-2),(x-1,y+2),(x-1,y-2)]
    for items in full:
        if ((items[0] > 7) or (items[0] < 0) or (items[1] > 7) or (items[1] < 0)):
            full.remove(items)
    return full

def raw_possible_moves_bishop(position):
    x,y = position.x, position.y
    byx = x
    byy = y
    full = []
    while  (byx < 7) and (byy < 7):
        byx += 1
        byy += 1
        full.append((byx,byy))
    byx = x
    byy = y
    while  (byx > 0) and (byy > 0):
        byx -= 1
        byy -= 1
        full.append((byx,byy))
    byx = x
    byy = y
    while  (byx < 7) and (byy > 0):
        byx += 1
        byy -= 1
        full.append((byx,byy))
    byx = x
    byy = y
    while  (byx > 0) and (byy < 7):
        byx -= 1
        byy += 1
        full.append((byx,byy))
    return full

def raw_possible_moves_queen(position):
    full = raw_possible_moves_rook(position).extend(raw_possible_moves_bishop(position))
    return full