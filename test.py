import unittest

from board import Board, Coordinates
from const import *

from operations import raw_possible_moves_king, raw_possible_moves_knight, raw_possible_moves_rook, raw_possible_moves_bishop, raw_possible_moves_queen, raw_possible_moves_pawn


def empty_board():
    board = Board()
    for i in range(8):
        for j in range(8):
            board.put(Coordinates(i, j), None)
    return board


class TestAll(unittest.TestCase):
    def test_coordinates(self):
        word = 'e2'
        coord = Coordinates.from_string(word)
        self.assertEqual(coord.x, 4)
        self.assertEqual(coord.y, 1)
        self.assertEqual(str(coord), word)

        a1 = Coordinates.from_string('a1')
        self.assertFalse(a1.left())
        self.assertTrue(str(a1.right()))
        self.assertEqual(str(a1.right()), 'b1')
        self.assertFalse(a1.bottom())
        self.assertEqual(str(a1.top()), 'a2')
        self.assertFalse(a1.top_left())
        self.assertEqual(str(a1.top_right()), 'b2')


    def test_possible_moves(self):
        self.empty_board = empty_board()
        self.full_board = Board()

        # raw possible moves

        # king
        moves = sorted(raw_possible_moves_king(Coordinates.from_string('a1')), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a2', 'b1', 'b2'])

        moves = sorted(raw_possible_moves_king(Coordinates.from_string('e5')), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['d4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'])

        # knight
        moves = sorted(raw_possible_moves_knight(Coordinates.from_string('b1')), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a3', 'c3', 'd2'])

        moves = sorted(raw_possible_moves_knight(Coordinates.from_string('a1')), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['b3', 'c2'])

        moves = sorted(raw_possible_moves_knight(Coordinates.from_string('c3')), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a2', 'a4', 'b1', 'b5', 'd1', 'd5', 'e2', 'e4'])

        # rook
        moves = sorted(raw_possible_moves_rook(Coordinates.from_string('d3'), self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a3', 'b3', 'c3', 'd1', 'd2', 'd4', 'd5', 'd6', 'd7', 'd8', 'e3', 'f3', 'g3', 'h3'])

        moves = sorted(raw_possible_moves_rook(Coordinates.from_string('a1'), self.full_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a2', 'b1'])

        # bishop
        moves = sorted(raw_possible_moves_bishop(Coordinates.from_string('a3'), self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['b2', 'b4', 'c1', 'c5', 'd6', 'e7', 'f8'])

        moves = sorted(raw_possible_moves_bishop(Coordinates.from_string('h1'), self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a8', 'b7', 'c6', 'd5', 'e4', 'f3', 'g2'])

        # queen
        moves = sorted(raw_possible_moves_queen(Coordinates.from_string('e1'), self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a1', 'a5', 'b1', 'b4', 'c1', 'c3', 'd1', 'd2', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'g1', 'g3', 'h1', 'h4'])

        moves = sorted(raw_possible_moves_queen(Coordinates.from_string('d1'), self.full_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['c1', 'c2', 'd2', 'e1', 'e2'])

        # pawn
        moves = sorted(raw_possible_moves_pawn(Coordinates.from_string('h7'), self.full_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['h5', 'h6'])

        # all possible moves
        
        


    def test_board(self):
        board = Board()
        all_figures = board.all_figures()
        self.assertEqual(len(all_figures), 32)
        only_white_queens = list(filter(lambda item: item[0].type == QUEEN and item[0].color == WHITE, all_figures))
        self.assertEqual(len(only_white_queens), 1)
        wq = only_white_queens[0]
        self.assertEqual(str(wq[1]), 'd1')

        self.assertEqual(len(board.white_figures()), 16)


if __name__ == "__main__":
    unittest.main()
