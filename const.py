WHITE = "White"
BLACK = "Black"

ONEPLAYER = 0
TWOPLAYERS = 1

MAX_IDLE_MOVES = 50
MAX_REPETITIONS = 3

PAWN = 'PAWN'
ROOK = 'ROOK'
KNIGHT = 'KNIGHT'
BISHOP = 'BISHOP'
QUEEN = 'QUEEN'
KING = 'KING'

WHITE_WIN = "White"
BLACK_WIN = "Black"
TIE = "TIE"

COMMON_MOVE = "common_move"
CASTLING_MOVE = "castling_move"
E_P_MOVE = "e_p_move"

CASTLING_DATA = {
    'e1g1': {
        'rook_move': ('h1', 'f1'),
        'inner_fields': ['f1', 'g1'],
        'safe_fields': ['e1', 'f1', 'g1'],
        'color': WHITE
    },
    'e8g8': {
        'rook_move': ('h8', 'f8'),
        'inner_fields': ['f8', 'g8'],
        'safe_fields': ['e8', 'f8', 'g8'],
        'color': BLACK
    },
    'e1c1': {
        'rook_move': ('a1', 'd1'),
        'inner_fields': ['b1', 'c1', 'd1'],
        'safe_fields': ['e1', 'd1', 'c1'],
        'color': WHITE
    },
    'e8c8': {
        'rook_move': ('a8', 'd8'),
        'inner_fields': ['b8', 'c8', 'd8'],
        'safe_fields': ['e8', 'd8', 'c8'],
        'color': BLACK
    }
}

# FIXME: this

INDEX_TO_LETTER = {
0 : 'a',
1 : 'b',
2 : 'c',
3 : 'd',
4 : 'e',
5 : 'f',
6 : 'g',
7 : 'h'}

LETTER_TO_INDEX = {'A' : 0,
         'B' : 1,
         'C' : 2,
         'D' : 3,
         'E' : 4,
         'F' : 5,
         'G' : 6,
         'H' : 7,
         'a' : 0,
         'b' : 1,
         'c' : 2,
         'd' : 3,
         'e' : 4,
         'f' : 5,
         'g' : 6,
         'h' : 7}

LOGDIR = 'logs'
LOG_FILE_PATTERN = "log.txt.{0}"

WIN_IMAGE = 'img/fail.jpg'
TIE_IMAGE = 'img/tie.jpg'
INITIAL_BACKGROUND = 'img/fon.jpg'
GAME_BACKGROUND ='img/fon2.jpg'
FONT = 'img/11895.ttf'
FAIL = 'img/11464.ttf'

NOTHING = 'img/nothing.png'
figuretypeback = {
  '_pawn.png'   : PAWN,
  '_rook.png'   : ROOK,
  '_knight.png' : KNIGHT,
  '_bishop.png' : BISHOP,
  '_queen.png'  : QUEEN,
  '_king.png'   : KING
}

figuretype = {
              PAWN    : '_pawn.png',
              ROOK    : '_rook.png',
              KNIGHT  : '_knight.png',
              BISHOP  : '_bishop.png',
              QUEEN   : '_queen.png',
              KING    : '_king.png'
             }
figurecolor = {WHITE : 'img/w',BLACK : 'img/b'}

# orientation
REGULAR = True
INVERSE = False

# FIXME: this

listoflaters = ['A','B','C','D','E','F','G','H']

COLOROFCELL1 = [.6,.3,0,1]
COLOROFCELL2 = [.8,.7,.6,1]
INITIAL_BUTTON_COLOR = [.97,.69,.59,1]
GAME_BUTTON_COLOR = [.39,.2,0,1]
BACKGROUND =  [.39,.2,0,1]
BACKGROUND1 =  [.69,.69,.68,1]



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
