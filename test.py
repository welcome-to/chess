import unittest

from Board import Coordinates

from operations import possible_moves_king


class TestAll(unittest.TestCase):
    def test_coordinates(self):
        word = 'e2'
        coord = Coordinates.from_string(word)
        self.assertEqual(coord.x, 4)
        self.assertEqual(coord.y, 1)
        self.assertEqual(str(coord), word)

    def test_possible_moves(self):
        moves = 


if __name__ == "__main__":
    unittest.main()
