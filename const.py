WHITE = 0
BLACK = 1


COLOROFCELL1 = [150/255,75/255,0/255,1]
COLOROFCELL2 = [.8,.7,.6,1]
INITIAL_BUTTON_COLOR = [248/255,176/255,152/255,1]
GAME_BUTTON_COLOR = [100/255,50/255,0/255,1]
BACKGROUND =  [100/255,50/255,0/255,1]
BACKGROUND1 =  [177/255,177/255,175/255,1]

PAWN = 'PAWN'
ROOK = 'ROOK'
KNIGHT = 'KNIGHT'
BISHOP = 'BISHOP'
QUEEN = 'QUEEN'
KING = 'KING'

WHITE_WIN = 0
BLACK_WIN = 1
TIE = 2

WHITE_WIN_IMAGE = 'img/kkk.jpg'
BLACK_WIN_IMAGE = 'img/fail.jpg'
TIE_IMAGE = 'img/tie.jpg'
INITIAL_BACKGROUND = 'img/fon.jpg'
GAME_BACKGROUND ='img/fon2.jpg'
FONT = 'img/11895.ttf'
FAIL = 'img/11464.ttf'

listoflaters = ['A','B','C','D','E','F','G','H']

# orientation
REGULAR = True
INVERSE = False

CASTLING_DATA = {
    'e1g1': {
        'rook_move': 'h1f1',
        'inner_fields': ['f1', 'g1'],
        'safe_fields': ['e1', 'f1', 'g1'],
        'color': WHITE
    },
    'e8g8': {
        'rook_move': 'h8f8',
        'inner_fields': ['f8', 'g8'],
        'safe_fields': ['e8', 'f8', 'g8'],
        'color': BLACK
    },
    'e1c1': {
        'rook_move': 'a1d1',
        'inner_fields': ['b1', 'c1', 'd1'],
        'safe_fields': ['e1', 'd1', 'c1'],
        'color': WHITE
    },
    'e8c8': {
        'rook_move': 'a8d8',
        'inner_fields': ['b8', 'c8', 'd8'],
        'safe_fields': ['e8', 'd8', 'c8'],
        'color': BLACK
    }
}

INDEX_TO_LETTER = {0:'a',
1 : 'b',
2 : 'c',
3 : 'd',
4 :'e',
5 :'f',
6 :'g',
7 :'h'}
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


sourcelist = [
['img/w_rook.png','img/w_knight.png','img/w_bishop.png','img/w_king.png','img/w_queen.png','img/w_bishop.png','img/w_knight.png','img/w_rook.png'],
['img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png'],
['img/b_rook.png','img/b_knight.png','img/b_bishop.png','img/b_king.png','img/b_queen.png','img/b_bishop.png','img/b_knight.png','img/b_rook.png']]


LOGDIR = 'logs'
LOG_FILE_PATTERN = "log.txt.{0}"
