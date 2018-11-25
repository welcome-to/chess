import unittest

from board import Board, Coordinates, Figure, Move, figures_on_board
from const import *
from exception import InternalError, InvalidMove

from operations import create_move, game_status, is_castling, is_castling_correct, is_e_p, is_kamikadze, is_pawn_jump
from possible_moves import *

from decode import decode_move, decode_game


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


class TestEngine(unittest.TestCase):
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


    def test_e_p(self):
        board = empty_board()
        wp1 = Figure(WHITE, PAWN)
        wp2 = Figure(WHITE, PAWN)
        bp = Figure(BLACK, PAWN)
        board.put(E4, wp1)
        board.put(E5, wp2)
        board.put(D4, bp)
        self.assertTrue(is_e_p(E4, D5, board))
        self.assertFalse(is_e_p(D4, E5, board))


    def test_castling(self):
        board = Board()
        self.assertTrue(is_castling(E1, C1, board))
        self.assertFalse(is_castling(G8, E8, board))
        board.move(H8, E8)
        self.assertFalse(is_castling(E8, C8, board))

        # FIXME: assertRaises for incorrect Move object

        board = empty_board()
        king = Figure(BLACK, KING)
        rook = Figure(BLACK, ROOK)
        board.put(E8, king)
        board.put(H8, rook)
        self.assertTrue(is_castling_correct(create_move(E8, G8, board, BLACK), board, BLACK))
        with self.assertRaises(InvalidMove):
            result = is_castling_correct(create_move(E1, G1, board, WHITE), board, WHITE)

        enemy_queen = Figure(WHITE, QUEEN)
        board.put(E3, enemy_queen)
        self.assertFalse(is_castling_correct(create_move(E8, G8, board, BLACK), board, BLACK))
        board.move(E3, F3)
        self.assertFalse(is_castling_correct(create_move(E8, G8, board, BLACK), board, BLACK))

        pawn = Figure(BLACK, PAWN)
        board.put(F6, pawn)
        self.assertTrue(is_castling_correct(create_move(E8, G8, board, BLACK), board, BLACK))


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


class TestDecode(unittest.TestCase):
    def test_decode_move(self):
        board = Board()
        self.assertEqual(decode_move('e4', board, WHITE, None), 'e2e4')
        board.move(E2, E4)
        self.assertEqual(decode_move('e5', board, BLACK, None), 'e7e5')
        board.move(E7, E5)
        self.assertEqual(decode_move('Bc4', board, WHITE, None), 'f1c4')
        board.move(F1, C4)
        self.assertEqual(decode_move('Nc6', board, BLACK, None), 'b8c6')
        board.move(B8, C6)
        self.assertEqual(decode_move('Qh5', board, WHITE, None), 'd1h5')
        board.move(D1, H5)
        self.assertEqual(decode_move('Nf6', board, BLACK, None), 'g8f6')
        board.move(G8, F6)
        self.assertEqual(decode_move('Qxf7#', board, WHITE, None), 'h5f7')

    def test_decode_line(self):
        line = "1.g3 Nf6 2.Bg2 g6 3.d4 Bg7 4.Nf3 0-0 5.0-0 d6 6.c3 Nbd7 7.Na3 c6 8.b4 Re8 9.Nc4 Nb6 10.Ne3 Nfd5 " + \
            "11.Qc2 Nxe3 12.fxe3 d5 13.e4 a5 14.e5 Bf5 15.Qb3 axb4 16.cxb4 Nc4 17.Ng5 f6 18.e4 Bc8 19.exd5 cxd5 20.Qf3 Nb6 " + \
            "21.Nh3 fxe5 22.dxe5 Rf8 23.Bf4 Bxe5 24.Rad1 Bxf4 25.Nxf4 e5 26.Qb3 exf4 27.Bxd5+ Nxd5 28.Rxd5 Qb6+ 29.Rc5+ Be6 30.Qc3 fxg3 " + \
            "31.Rxf8+ Rxf8 32.hxg3 Qd6 0-1"
        game = decode_game(line)

    def test_decode_line_2(self):
        line = "1.d4 Nf6 2.Nf3 c5 3.d5 d6 4.Nc3 g6 5.e4 Bg7 6.Bb5+ Bd7 7.a4 0-0 8.0-0 Bxb5 9.axb5 Nbd7 10.h3 Qc7 " + \
               "11.Bf4 a6 12.Qe2 Qb6 13.Nd2 axb5 14.Qxb5 Qxb5 15.Nxb5 Nh5 16.Bg5 Bf6 17.Bh6 Rfc8 18.g4 Ng7 19.c3 Nb6 20.Rxa8 Rxa8 " + \
               "21.g5 Be5 22.f4 Ra5 23.Nc7 Bxf4 24.Rxf4 c4 25.b4 cxb3 26.Nxb3 Ra3 27.Nd4 Rxc3 28.Bxg7 Kxg7 29.Nce6+ Kg8 30.Nd8 Rd3 " + \
               "31.Nxf7 Nd7 32.Nh6+ Kh8 33.Ne6 Rc3 34.Rf7 Rc1+ 35.Kf2 Rc8 36.Rxe7 Nc5 37.Nxc5 1-0"
        game = decode_game(line)


    def test_decode_line_3(self):
        line = "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.0-0 Be7 6.Re1 b5 7.Bb3 d6 8.c3 0-0 9.h3 Nb8 10.d4 Nbd7 " + \
               "11.Nbd2 Bb7 12.Bc2 Re8 13.Nf1 Bf8 14.Ng3 g6 15.b3 c6 16.Bg5 Qc7 17.Qd2 Bg7 18.Nh2 d5 19.dxe5 Nxe4 20.Bxe4 dxe4 " + \
               "21.Nxe4 h6 22.Nf6+ Nxf6 23.Bxf6 c5 24.Ng4 g5 25.Rad1 Qc6 26.f3 c4 27.Qd4 Bf8 28.b4 Re6 29.h4 h5 30.Qe3 hxg4 " + \
               "31.Qxg5+ Kh7 32.Qh5+ Bh6 33.Qxf7+ 1-0"
        game = decode_game(line)


    def test_decode_line_4(self):
        line = "1.e4 Nf6 2.e5 Nd5 3.d4 d6 4.c4 Nb6 5.exd6 exd6 6.Nc3 Be7 7.Be2 0-0 8.Nf3 Nc6 9.0-0 Bg4 10.b3 Bf6 " + \
               "11.Be3 d5 12.c5 Nc8 13.b4 N8e7 14.h3 Bxf3 15.Bxf3 Nxb4 16.Rb1 Nbc6 17.Rxb7 Na5 18.Rb4 c6 19.Bf4 Nc4 20.Qd3 g6 " + \
               "21.g4 g5 22.Bg3 Ng6 23.Ne2 Qa5 24.Rb7 Rae8 25.Nc3 Re6 26.Nxd5 Nd2 27.Nc7 Re1 28.Rxe1 Nxf3+ 29.Qxf3 Qxe1+ 30.Kg2 Bxd4 " + \
               "31.Na6 Be5 32.Nb4 Bxg3 33.fxg3 Ne5 34.Qf2 Qe4+ 35.Kf1 f5 36.Qe2 fxg4+ 37.Ke1 Nf3+ 0-1"
        game = decode_game(line)


    def test_decode_line_5(self):
        line = "1.e4 c6 2.d4 d5 3.Nc3 dxe4 4.Nxe4 Bf5 5.Ng3 Bg6 6.h4 h6 7.Nf3 Nd7 8.h5 Bh7 9.Bd3 Bxd3 10.Qxd3 e6 " + \
               "11.Bf4 Qa5+ 12.Bd2 Bb4 13.c3 Be7 14.c4 Qc7 15.Qe2 Ngf6 16.0-0-0 0-0 17.Ne5 Nxe5 18.dxe5 Nd7 19.f4 b5 20.Ne4 Rab8 " + \
               "21.Rh3 bxc4 22.Qxc4 Nb6 23.Qc2 Nd5 24.Rf1 Bb4 25.a3 Bxd2+ 26.Nxd2 c5 27.Nc4 Nb6 28.Nd6 c4 29.Rc3 Qc5 30.Ne4 Qa5 " + \
               "31.Rg3 Kh8 32.Nc3 Nd5 33.Qe2 Rb3 34.Qg4 Rg8 35.Nxd5 Qxd5 36.Rff3 Rd3 37.Rxd3 cxd3 38.Kd2 Qb3 39.Rxd3 Qxb2+ 40.Ke3 Qc1+ " + \
               "41.Kf3 Qf1+ 42.Ke3 Qe1+ 43.Qe2 Qg1+ 44.Qf2 Qh1 45.Qe2 Rb8 46.Kf2 Qh4+ 47.Ke3 Rb1 48.Qf3 Qe1+ 49.Qe2 Qg1+ 50.Kf3 Qb6 " + \
               "51.Qd2 Rb3 52.Kg4 Rxd3 53.Qxd3 Qa5 1/2"
        game = decode_game(line)


    def test_decode_line_6(self):
        line = "1.d4 d5 2.c4 c6 3.Nf3 e6 4.e3 Nf6 5.Nc3 a6 6.c5 b6 7.cxb6 Nbd7 8.Bd2 a5 9.Rc1 Qxb6 10.Na4 Qc7 " + \
               "11.Qc2 Bb7 12.Bd3 Be7 13.0-0 Ba6 14.Ne1 Bxd3 15.Nxd3 Rc8 16.Qc3 Bd8 17.f3 0-0 18.Be1 Qa7 19.Bg3 Be7 20.Rc2 Nb6 " + \
               "21.Nxb6 Qxb6 22.Rfc1 Nd7 23.Qb3 Qa6 24.Rc3 a4 25.Qc2 Qb5 26.Ne5 Nxe5 27.Bxe5 Bb4 28.Rd3 Rfd8 29.a3 Bd6 30.Bxd6 Rxd6 31.b4 axb3 " + \
               "32.Rxb3 Qa6 33.Qc5 Rdd8 34.Kf2 g6 35.Rb6 Qa4 36.Qb4 Ra8 37.Qxa4 Rxa4 38.Rc3 Rda8 39.Rbb3 Kg7 40.Ke2 h5 " + \
               "41.Kd2 Kf6 42.Kc2 R4a6 43.Kb2 g5 44.Rb7 g4 45.f4 h4 46.Ka2 Rc8 47.Kb3 Rca8 48.Ka2 Rc8 49.Kb3 Rca8 50.Ka2 1/2"
        game = decode_game(line)



if __name__ == "__main__":
    unittest.main()
