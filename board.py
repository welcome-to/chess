from const import *
from exception import InvalidMove, NotImplementedError, InternalError


class Figure(object):
    def __init__(self, color, type):
        self.color = color
        self.has_moved = False
        self.type = type

    def __str__(self): #FIXME
        return self.type


class Move(object):
    def __init__(self, line, is_roque=False):
        self.start = Coordinates.from_string(line[:2])
        self.end = Coordinates.from_string(line[2:])
        self.is_roque = is_roque

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

    def __str__(self):
        index_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        try:
            return "{0}{1}".format(index_to_letter[self.x], self.y + 1)
        except:
            raise InternalError("?")


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

    def put(self, position, figure):
        self.data[position.y][position.x] = figure

    def pop(self, position):
        figure = self.figure_on_position(position.x, position.y)
        if figure is None:
            raise InvalidMove("No figure at {0}".format(start))
        self.data[position.y][position.x] = None
        return figure

    def move(self, start, end):
        figure = self.pop(start)
        self.put(end, figure)

    def figure_on_position(self, x, y):
        return self.data[y][x]

    def all_figures(self):
        all_figures = []
        for row in range(8):
            for cell in range(8):
                if self.data[row][cell] != None:
                    all_figures.append((self.data[row][cell],Coordinates(cell,row)))
        return all_figures

    def white_figures(self):
        return list(filter(lambda item: item[0].color == WHITE, self.all_figures()))

    def black_figures(self):
        return list(filter(lambda item: item[0].color == BLACK, self.all_figures()))

    def __str__(self):
        return '\n'.join(reversed(
            [' '.join(str(element) for element in lst) for lst in self.data]
        ))
