from const import *
from exception import InvalidMove, NotImplementedError, InternalError


class Figure(object):
    def __init__(self, color, type):
        self.color = color
        self.has_moved = False
        self.type = type

    def __repr__(self):
        return "{0}|{1}".format({WHITE: "W", BLACK: "B"}[self.color], self.type)


class Move(object):
    def __init__(self, start, end, is_roque=False):
        self.start = start
        self.end = end
        self.is_roque = is_roque

    @staticmethod
    def from_string(line):
        try:
            return Move(Coordinates.from_string(line[:2]), Coordinates.from_string(line[2:]))
        except:
            raise InvalidMove("Incorrect input: {0}".format(line))

    def __repr__(self):
        return str(self.start) + str(self.end)


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


class Board(object):
    def __init__(self):
        self.data = [[None] * 8 for i in range(8)]
        for i in range(8):
            self.data[1][i] = Figure(WHITE, PAWN)
            self.data[6][i] = Figure(BLACK, PAWN)

        self.data[0][0] = Figure(WHITE, ROOK)
        self.data[0][7] = Figure(WHITE, ROOK)
        self.data[7][0] = Figure(BLACK, ROOK)
        self.data[7][7] = Figure(BLACK, ROOK)

        self.data[0][1] = Figure(WHITE, KNIGHT)
        self.data[0][6] = Figure(WHITE, KNIGHT)
        self.data[7][1] = Figure(BLACK, KNIGHT)
        self.data[7][6] = Figure(BLACK, KNIGHT)

        self.data[0][2] = Figure(WHITE, BISHOP)
        self.data[0][5] = Figure(WHITE, BISHOP)
        self.data[7][2] = Figure(BLACK, BISHOP)
        self.data[7][5] = Figure(BLACK, BISHOP)

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
            raise InvalidMove("No figure at {0}".format(start))
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
        try:
            return self.data[coordinates.y][coordinates.x]
        except:
            raise InternalError("Received the following coordinates: x={0} y={1}. Will fail.".format(coordinates.x, coordinates.y))

    def all_figures(self):
        return self.all_figures_on

    def __str__(self):
        return '\n'.join(reversed(
            [' '.join(str(element) for element in lst) for lst in self.data]
        ))


def figures_on_board(board, type=None, color=None):
    result = board.all_figures()
    if color is not None:
        result = list(filter(lambda item: item[0].color == color, result))
    if type is not None:
        result = list(filter(lambda item: item[0].type == type, result))
    return result
