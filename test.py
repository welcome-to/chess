import unittest

from board import Board, Coordinates

from operations import raw_possible_moves_king


class TestAll(unittest.TestCase):
    def test_coordinates(self):
        word = 'e2'
        coord = Coordinates.from_string(word)
        self.assertEqual(coord.x, 4)
        self.assertEqual(coord.y, 1)
        self.assertEqual(str(coord), word)

    def test_possible_moves(self):
        pass

    def test_board(self):
        board = Board()
        all_figures = board.all_figures()
        self.assertEqual(len(all_figures), 32)


if __name__ == "__main__":
    unittest.main()
