WHITE = 0
BLACK = 1


COLOROFCELL1 = [1,0,0,1]
COLOROFCELL2 = [.8,.7,.6,1]
BUTTONCOLOR = [.3,.5,.7,1]

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
BLACK_WIN_IMAGE = 'img/mandela.jpg'
TIE_IMAGE = 'tie.jpg'


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
['img/w_rook.png','img/w_knight.png','img/w_bishop.png','img/w_queen.png','img/w_king.png','img/w_bishop.png','img/w_knight.png','img/w_rook.png'],
['img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png','img/w_pawn.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png','img/nothing.png'],
['img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png','img/b_pawn.png'],
['img/b_rook.png','img/b_knight.png','img/b_bishop.png','img/b_queen.png','img/b_king.png','img/b_bishop.png','img/b_knight.png','img/b_rook.png']]


