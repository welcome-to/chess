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
figurecolor = {0 : 'img/w',1 : 'img/b'}


sourcelist = [
['img/w_rook.png','img/w_knight.png','img/w_bishop.png','img/w_queen.png','img/w_king.png','img/w_bishop.png','img/w_knight.png','img/w_rook.png'],
['img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png'],
['img/b_rook.png','img/b_knight.png','img/b_bishop.png','img/b_queen.png','img/b_king.png','img/b_bishop.png','img/b_knight.png','img/b_rook.png']]


