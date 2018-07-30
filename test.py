import unittest

from board import Board, Coordinates
from const import *

from operations import raw_possible_moves_king


class TestAll(unittest.TestCase):
    def test_coordinates(self):
        word = 'e2'
        coord = Coordinates.from_string(word)
        self.assertEqual(coord.x, 4)
        self.assertEqual(coord.y, 1)
        self.assertEqual(str(coord), word)

        a1 = Coordinates.from_string('a1')
        self.assertEqual(a1.left(), None)
        self.assertTrue(a1.valid())
        self.assertEqual(str(a1.right()), 'b1')
        self.assertEqual(a1.bottom(), None)
        self.assertEqual(str(a1.top()), 'a2')
        self.assertEqual(a1.top_left(), None)
        self.assertEqual(str(a1.top_right()), 'b2')


    def test_possible_moves(self):
        king_position = Coordinates.from_string('a1')
        moves = sorted(raw_possible_moves_king(king_position), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a2', 'b1', 'b2'])

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
