import unittest

from board import Board, Coordinates, Figure, Move, figures_on_board
from const import *
from exception import InternalError

from operations import game_status, is_kamikadze, is_pawn_jump
from possible_moves import *


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


def children_board():
    board = Board()
    board.move(E2, E4)
    board.move(E7, E5)
    board.move(D1, H5)
    board.move(B8, C6)
    board.move(F1, C4)
    board.move(G8, F6)
    board.move(H5, F7)
    return board


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
        moves = sorted(raw_possible_moves_king(A1), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a2', 'b1', 'b2'])

        moves = sorted(raw_possible_moves_king(E5), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['d4', 'd5', 'd6', 'e4', 'e6', 'f4', 'f5', 'f6'])

        # knight
        moves = sorted(raw_possible_moves_knight(B1), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a3', 'c3', 'd2'])

        moves = sorted(raw_possible_moves_knight(A1), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['b3', 'c2'])

        moves = sorted(raw_possible_moves_knight(C3), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a2', 'a4', 'b1', 'b5', 'd1', 'd5', 'e2', 'e4'])

        # rook
        moves = sorted(raw_possible_moves_rook(D3, self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a3', 'b3', 'c3', 'd1', 'd2', 'd4', 'd5', 'd6', 'd7', 'd8', 'e3', 'f3', 'g3', 'h3'])

        moves = sorted(raw_possible_moves_rook(A1, self.full_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a2', 'b1'])

        # bishop
        moves = sorted(raw_possible_moves_bishop(A3, self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['b2', 'b4', 'c1', 'c5', 'd6', 'e7', 'f8'])

        moves = sorted(raw_possible_moves_bishop(H1, self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a8', 'b7', 'c6', 'd5', 'e4', 'f3', 'g2'])

        # queen
        moves = sorted(raw_possible_moves_queen(E1, self.empty_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['a1', 'a5', 'b1', 'b4', 'c1', 'c3', 'd1', 'd2', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'f1', 'f2', 'g1', 'g3', 'h1', 'h4'])

        moves = sorted(raw_possible_moves_queen(D1, self.full_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['c1', 'c2', 'd2', 'e1', 'e2'])

        # pawn
        moves = sorted(raw_possible_moves_pawn(H7, self.full_board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['h5', 'h6'])

        board = empty_board()
        board.put(E4, Figure(WHITE, PAWN))
        board.put(D7, Figure(BLACK, PAWN))
        board.move(D7, D4)
        moves = sorted(raw_possible_moves_pawn(D4, board), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['d3'])

        # all possible moves
        pass


    def test_game_status(self):
        ch_board = children_board()
        self.assertEqual(game_status(ch_board, BLACK, None), WHITE_WIN)


    def test_board(self):
        board = Board()
        all_figures = board.all_figures()
        self.assertEqual(len(all_figures), 32)
        only_white_queens = list(filter(lambda item: item[0].type == QUEEN and item[0].color == WHITE, all_figures))
        self.assertEqual(len(only_white_queens), 1)
        wq = only_white_queens[0]
        self.assertEqual(str(wq[1]), 'd1')

        self.assertEqual(len(figures_on_board(board, color=WHITE)), 16)


    def test_is_pawn_jump(self):
        board = Board()
        board.move(E2, E4)
        board.move(D2, D3)
        board.move(H7, H5)
        self.assertTrue(is_pawn_jump(board, Move(E2, E4), WHITE))
        self.assertFalse(is_pawn_jump(board, Move(D2, D3), WHITE))
        self.assertTrue(is_pawn_jump(board, Move(H7, H5), BLACK))
        with self.assertRaises(InternalError):
            is_pawn_jump(board, Move(H6, H4), BLACK)


    def test_kamikadze(self):
     # first move is correct
        self.assertEqual(
            is_kamikadze(Board(), Move(E2, E4, type=COMMON_MOVE), None),
            False
        )

        bad_board = Board()
        bad_board.pop(E2)
        bad_board.move(A8, E6) # шах
        self.assertEqual(
            is_kamikadze(bad_board, Move(B2, B4, type=COMMON_MOVE), None),
            True
        )

        ch_board = children_board()

        self.assertEqual(
            is_kamikadze(ch_board, Move(E8, E7, type=COMMON_MOVE), Move(H5, F7, type=COMMON_MOVE)),
            True
        )
        self.assertEqual(
            is_kamikadze(ch_board, Move(D7, D5, type=COMMON_MOVE), Move(H5, F7, type=COMMON_MOVE)),
            True
        )
        self.assertEqual(
            is_kamikadze(ch_board, Move(C6, D4, type=COMMON_MOVE), Move(H5, F7, type=COMMON_MOVE)),
            True
        )

        board = Board()
        board.move(E2, E4)
        board.move(G8, F6)
        board.move(A2, A3)
        board.move(F6, E4)
        board.move(E1, E2)
        board.move(E4, G3) # жена упала, Штирлиц насторожился
        self.assertEqual(
            is_kamikadze(board, Move(B2, B4, type=COMMON_MOVE), Move(E4, G3, type=COMMON_MOVE)),
            True
        )

        board = empty_board()
        king = Figure(BLACK, KING)
        enemy_queen = Figure(WHITE, QUEEN)
        board.put(D4, king)
        board.put(E4, enemy_queen)
        self.assertEqual(
            is_kamikadze(board, Move(D4, C3, type=COMMON_MOVE), None),
            False
        )

        board = empty_board()
        board.put(D4, Figure(BLACK, KING))
        board.put(A4, Figure(WHITE, QUEEN))
        board.put(B4, Figure(WHITE, PAWN))
        board.put(C4, Figure(BLACK, PAWN))
        self.assertEqual(
            is_kamikadze(board, Move(C4, B3, type=E_P_MOVE, eaten_position=B4), Move(B2, B4, type=COMMON_MOVE)),
            True
        )


if __name__ == "__main__":
    unittest.main()
