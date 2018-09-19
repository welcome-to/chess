import unittest
import cProfile
from board import Board, Coordinates, Figure, Move, figures_on_board
from const import *
from exception import *

from operations import (
    raw_possible_moves_king, raw_possible_moves_knight, raw_possible_moves_rook,
    raw_possible_moves_bishop, raw_possible_moves_queen, raw_possible_moves_pawn,
    IsKamikadze, game_status, is_castling, is_castling_correct, is_correct, is_pawn_jump, is_e_p, make_e_p
)

from run import GameProcessor


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


def empty_board():
    board = Board()
    for i in range(8):
        for j in range(8):
            board.put(Coordinates(i, j), None)
    return board


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
        moves = sorted(raw_possible_moves_pawn(H7, self.full_board, None), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['h5', 'h6'])

        board = empty_board()
        board.put(E4, Figure(WHITE, PAWN))
        board.put(D7, Figure(BLACK, PAWN))
        board.move(D7, D4)
        moves = sorted(raw_possible_moves_pawn(D4, board, Move(E2, E4)), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['d3', 'e3'])
        board.put(A5, Figure(WHITE, PAWN))
        moves = sorted(raw_possible_moves_pawn(D4, board, Move(A4, A5)), key=lambda x: str(x))
        self.assertEqual(list(map(str, moves)), ['d3'])

        # all possible moves
        pass


    def test_castling(self):
        board = Board()
        self.assertTrue(is_castling(Move(E1, C1), board))
        self.assertFalse(is_castling(Move(G8, E8), board))
        board.move(H8, E8)
        self.assertFalse(is_castling(Move(E8, C8), board))

        board = empty_board()
        king = Figure(BLACK, KING)
        rook = Figure(BLACK, ROOK)
        board.put(E8, king)
        board.put(H8, rook)
        self.assertTrue(is_castling_correct(Move(E8, G8), board, BLACK))
        self.assertFalse(is_castling_correct(Move(E1, G1), board, WHITE))

        enemy_queen = Figure(WHITE, QUEEN)
        board.put(E3, enemy_queen)
        self.assertFalse(is_castling_correct(Move(E8, G8), board, BLACK))
        board.move(E3, F3)
        self.assertFalse(is_castling_correct(Move(E8, G8), board, BLACK))

        pawn = Figure(BLACK, PAWN)
        board.put(F6, pawn)
        self.assertTrue(is_castling_correct(Move(E8, G8), board, BLACK))


    def test_kamikadze(self):
        # first move is correct
        self.assertEqual(IsKamikadze(Board(), E2)(E4), False)

        bad_board = Board()
        bad_board.pop(E2)
        bad_board.move(A8, E6) # шах
        self.assertEqual(IsKamikadze(bad_board, B2)(B4), True)

        ch_board = children_board()
        self.assertEqual(IsKamikadze(ch_board, E8)(E7), True)
        self.assertEqual(IsKamikadze(ch_board, D7)(D5), True)
        self.assertEqual(IsKamikadze(ch_board, C6)(D4), True)

        board = Board()
        board.move(E2, E4)
        board.move(G8, F6)
        board.move(A2, A3)
        board.move(F6, E4)
        board.move(E1, E2)
        board.move(E4, G3) # жена упала, Штирлиц насторожился
        self.assertEqual(IsKamikadze(board, B2)(B4), True)

        board = empty_board()
        king = Figure(BLACK, KING)
        enemy_queen = Figure(WHITE, QUEEN)
        board.put(D4, king)
        board.put(E4, enemy_queen)
        self.assertEqual(IsKamikadze(board, D4)(C3), False)


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


    def test_is_correct(self):
        board = empty_board()
        wp1 = Figure(WHITE, PAWN)
        wp2 = Figure(WHITE, PAWN)
        wb = Figure(WHITE, BISHOP)
        wk = Figure(WHITE, KING)
        bp1 = Figure(BLACK, PAWN)
        bp2 = Figure(BLACK, PAWN)
        bp3 = Figure(BLACK, PAWN)
        bn = Figure(BLACK, KNIGHT)
        bk = Figure(BLACK, KING)
        board.put(E4, wp1)
        board.put(A4, wp2)
        board.put(B1, wb)
        board.put(D3, wk)
        board.put(F3, bn)
        board.put(G5, bp1)
        board.put(F6, bp2)
        board.put(A7, bp3)
        board.put(B4, bk)
        self.assertTrue(is_correct(Move(D3, E3), board, WHITE, None))


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


    def test_e_p(self):
        board = empty_board()
        wp1 = Figure(WHITE, PAWN)
        wp2 = Figure(WHITE, PAWN)
        bp = Figure(BLACK, PAWN)
        board.put(E4, wp1)
        board.put(E5, wp2)
        board.put(D4, bp)
        self.assertTrue(is_e_p(Move(E4, D5), board))
        self.assertFalse(is_e_p(Move(D4, E5), board))

        self.assertTrue(board.figure_on_position(D5) is None)
        make_e_p(board, Move(E4, D5))
        wp = board.figure_on_position(D5)
        self.assertTrue(wp is not None)
        self.assertEqual(wp.type, PAWN)
        self.assertEqual(wp.color, WHITE)

    def test_57(self):
        #board = Board()
        gp = GameProcessor()
        gp.make_turn(H2, H3)
        gp.make_turn(E7, E6)
        gp.make_turn(A2, A4)
        gp.make_turn(F8, D6)
        gp.make_turn(E2, E4)
        gp.make_turn(F7, F6)
        gp.make_turn(B1, A3)
        gp.make_turn(D6, F4)
        gp.make_turn(H1, H2)
        gp.make_turn(E8, E7)
        gp.make_turn(E1, E2)
        gp.make_turn(B8, A6)
        gp.make_turn(A3, B5)
        gp.make_turn(C7, C5)
        gp.make_turn(A4, A5)
        gp.make_turn(D8, F8)
        gp.make_turn(E2, E1)
        gp.make_turn(F4, D2)
        print(gp.board)
        gp.make_turn(B5, C7)
        print("Game status: {0}".format(game_status(gp.board, BLACK, None)))


if __name__ == "__main__":
    #cProfile.run("unittest.main()")
    unittest.main()
