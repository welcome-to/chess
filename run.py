from copy import deepcopy
from const import *

class NotImplementedError(Exception):
    def __init__(self):
        self.value = "Not implemented"

    def __str__(self):
        return str(self.value)


class InvalidMove(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class InternalError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Figure(object):
    def __init__(self, color, type):
        self.color = color
        self.has_moved = False
        self.type = type

    def __str__(self): #FIXME
        return self.type


class AskTie(object):
    pass


class Move(object):
    """
    def __init__(self, start, end, is_roque=False):
        self.start = Coordinates.from_string(start)
        self.end = Coordinates.from_string(end)
        self.is_roque = is_roque
    """

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
        self.data[position.y][position.x] = None
        return figure

    def move(self, start, end):
        figure = self.pop(start)
        if figure is None:
            raise InvalidMove("No figure at {0}".format(start))
        self.put(end, figure)

    def figure_on_position(self, x, y):
        return self.data[y][x]

    def all_figures():
        raise NotImplementedError()

    def white_figures():
        raise NotImplementedError()

    def black_figures():
        raise NotImplementedError()

    def __str__(self):
        return '\n'.join(reversed(
            [' '.join(str(element) for element in lst) for lst in self.data]
        ))


class Algorithm(object):
    def __init__(self, name):
        self.name = name

    def make_turn(self, position):
        raise NotImplementedError()


class HumanPlayer(Algorithm):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)

    def __repr__(self):
        return str(self.name)

    def make_turn(self, board):
        line = input()
        return line


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


class GameProcessor(object):
    FILE_PATTERN = "./logs/game_{0}"

    def __init__(self):
        self.board = Board()
        self.boards = []
        self.turns = []
        # outside make_turn `current player' is the one whose turn is next
        self.current_player = WHITE
        self.next_player = BLACK

        self.technical_winner = None
        #self.log_file = open(FILE_PATTERN.format(datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%s")), "w")

    # `turn' is a line, either like `e2e4' or like `re1h1'
    def make_turn(self, command):
        try:
            if command.startswith('r'):
                turn = Move(command[1:], is_roque=True)
            else:
                turn = Move(command)
        except:
            self._run_technical_defeat()
            return

        self.turns.append(deepcopy(turn))

        if not is_correct(turn, self.board, self.current_player):
            self._run_technical_defeat()
            return

        if turn.is_roque:
            make_castling(self.board, turn)
        else: # move
            self.board.move(turn.start, turn.end)
        convert_pawns(self.board)
        self.boards.append(deepcopy(self.board))

        self.current_player, self.next_player = self.next_player, self.current_player

    def game_result(self):
        if self.technical_winner is not None:
            return self.technical_winner # dirty
        return game_status(self.board, self.current_player)

    def _run_technical_defeat(self):
        print("Invalid move")
        if self.current_player == WHITE:
            self.technical_winner = BLACK
        else:
            self.technical_winner = WHITE
    def savelog(self,bool):
        pass



def play(first, second):
    gp = GameProcessor()

    current_player = first
    next_player = second

    while gp.game_result() is None:
        print(gp.board)
        print("Player: {0}".format(current_player))
        print("Enter your turn. Example: 'e2 e4' or 'tie'")
        turn = current_player.make_turn(deepcopy(gp.board))
        gp.make_turn(turn)
        current_player, next_player = next_player, current_player

    return gp.game_result()



def print_result(game_result):
    print({
        0: "White win!",
        1: "Black win!",
        2: "Tie!"
    }[game_result])


if __name__ == "__main__":
    first = HumanPlayer("xyu1")
    second = HumanPlayer("xyu2")
    result = play(first, second)
    print_result(result)
