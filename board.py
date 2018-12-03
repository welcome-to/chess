from const import *
from exception import InvalidMove, NotImplementedError, InternalError


class Figure(object):
    def __init__(self, color, type):
        self.color = color
        self.has_moved = False
        self.type = type

    def __repr__(self):
        return "{0}|{1}".format(self.color, self.type)
    def __eq__(self,other_figure):
        if other_figure == None:
            return False
        if (self.color == other_figure.color) and \
           (self.type == other_figure.type) and \
           (self.has_moved == other_figure.has_moved):

            return True

        return False


class Move(object):
    def __init__(
        self, start, end,
        type=None,
        is_back_move=False,
        eaten_position=None,
        extra_move=None,
        lost_virginity=False,
        restored_figure=None
    ):
        if restored_figure is not None and eaten_position is None:
            raise RuntimeError("Look! Shit.")
        self.start = start
        self.end = end
        self.type = type
        self.is_back_move = is_back_move
        self.eaten_position = eaten_position
        self.extra_move = extra_move
        self.lost_virginity = lost_virginity
        self.restored_figure = restored_figure

    """
    @staticmethod
    def from_string(line):
        try:
            return Move(Coordinates.from_string(line[:2]), Coordinates.from_string(line[2:]))
        except:
            raise InvalidMove("Incorrect input: {0}".format(line))
    """
    def __repr__(self):
        result = str(self.start) + str(self.end)
        if self.eaten_position is not None:
            result += " eaten:" + str(self.eaten_position)
        return result


class Coordinates(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_string(line):
        try:
            return Coordinates(LETTER_TO_INDEX[line[0]], int(line[1]) - 1)
        except:
            raise InvalidMove("Incorrect input: {0}".format(line))

    def left(self):
        return Coordinates(self.x - 1, self.y)

    def right(self):
        return Coordinates(self.x + 1, self.y)

    def top(self):
        return Coordinates(self.x, self.y + 1)

    def bottom(self):
        return Coordinates(self.x, self.y - 1)

    def top_left(self):
        return self.left().top()

    def top_right(self):
        return self.right().top()

    def bottom_left(self):
        return self.left().bottom()

    def bottom_right(self):
        return self.right().bottom()

    def __bool__(self):
        return 0 <= self.x <= 7 and 0 <= self.y <= 7

    def __hash__(self):
        return hash(str(self))
        
    def __repr__(self):
        if not self:
            raise InternalError("Invalid coordinates")
        return "{0}{1}".format(INDEX_TO_LETTER[self.x], self.y + 1)

    def __eq__(self,other):
        if ((self.x == other.x) and (self.y == other.y)): 
            return True
        return False


A1, A2, A3, A4, A5, A6, A7, A8, \
B1, B2, B3, B4, B5, B6, B7, B8, \
C1, C2, C3, C4, C5, C6, C7, C8, \
D1, D2, D3, D4, D5, D6, D7, D8, \
E1, E2, E3, E4, E5, E6, E7, E8, \
F1, F2, F3, F4, F5, F6, F7, F8, \
G1, G2, G3, G4, G5, G6, G7, G8, \
H1, H2, H3, H4, H5, H6, H7, H8 = \
map(Coordinates.from_string, [
    'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8',
    'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8',
    'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8',
    'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8',
    'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
    'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8'
])


class Board(object):
    def __init__(self):
        self.data = [[None] * 8 for i in range(8)]
        for i in range(8):
            self.data[1][i] = Figure(WHITE, PAWN)
            self.data[6][i] = Figure(BLACK, PAWN)

        for i in range(2):
            self.data[0][i * 7] = Figure(WHITE, ROOK)
            self.data[7][i * 7] = Figure(BLACK, ROOK)

            self.data[0][1 + i * 5] = Figure(WHITE, KNIGHT)
            self.data[7][1 + i * 5] = Figure(BLACK, KNIGHT)

            self.data[0][2 + i * 3] = Figure(WHITE, BISHOP)
            self.data[7][2 + i * 3] = Figure(BLACK, BISHOP)

        self.data[0][3] = Figure(WHITE, QUEEN)
        self.data[7][3] = Figure(BLACK, QUEEN)
        self.data[0][4] = Figure(WHITE, KING)
        self.data[7][4] = Figure(BLACK, KING)
        self.updateselffigures()

    def put(self, position, figure):
        self.data[position.y][position.x] = figure
        self.updateselffigures()

    def pop(self, position):
        figure = self.figure_on_position(position)
        if figure is None:
            print(self)
            raise InvalidMove("No figure at {0}".format(position))
        self.data[position.y][position.x] = None
        self.updateselffigures()
        return figure

    def move(self, start, end):
        figure = self.pop(start)
        self.put(end, figure)
        figure.has_moved = True
        self.updateselffigures()

    def updateselffigures(self):
        self.all_figures_on = []
        for row in range(8):
            for cell in range(8):
                if self.data[row][cell] != None:
                    self.all_figures_on.append((self.data[row][cell],Coordinates(cell,row)))


    def figure_on_position(self, coordinates):
        # FIXME: this
        try:
            return self.data[coordinates.y][coordinates.x]
        except:
            raise InternalError("Received the following coordinates: x={0} y={1}. Will fail.".format(coordinates.x, coordinates.y))

    def all_figures(self):
        return self.all_figures_on

    def __str__(self):
        return '\n'.join(reversed(
            [' '.join(str(element).rjust(12, " ") for element in lst) for lst in self.data]
        ))
    def __eq__(self,other_board):
        for i in range(8):
            for j in range(8):
                if self.data[i][j] != other_board.data[i][j]:
                    return False
        return True


def figures_on_board(board, type=None, color=None):
    result = board.all_figures()
    if color is not None:
        result = list(filter(lambda item: item[0].color == color, result))
    if type is not None:
        result = list(filter(lambda item: item[0].type == type, result))
    return result
