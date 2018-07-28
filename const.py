WHITE = 0
BLACK = 1

PAWN = 'S'
ROOK = 'E'
KNIGHT = 'H'
BISHOP = 'O'
QUEEN = 'Q'
KING = 'K'

WHITE_WIN = 0
BLACK_WIN = 1
TIE = 2

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

figuretype = {'S'    : '_pawn.png',
              'E'    : '_rook.png',
              'H'  : '_knight.png',
              'O'  : '_bishop.png',
              'Q'   : '_queen.png',
              'K'    : '_king.png',
            }
figurecolor = {0 : 'w',1 : 'b'}


sourcelist = [
['w_rook.png','w_knight.png','w_bishop.png','w_queen.png','w_king.png','w_bishop.png','w_knight.png','w_rook.png'],
['w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png'],
['b_rook.png','b_knight.png','b_bishop.png','b_queen.png','b_king.png','b_bishop.png','b_knight.png','b_rook.png']]


