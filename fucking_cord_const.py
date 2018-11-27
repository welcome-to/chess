from board import Coordinates
from const import WHITE,BLACK

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


CASTLING_DATA = {
    (E1,G1): {
        'rook_move': (H1, F1),
        'inner_fields': [F1, G1],
        'safe_fields': [E1, F1, G1],
        'color': WHITE
    },
    (E8,G8): {
        'rook_move': (H8, F8),
        'inner_fields': [F8, G8],
        'safe_fields': [E8, F8, G8],
        'color': BLACK
    },
    (E1,C1): {
        'rook_move': (A1, D1),
        'inner_fields': [B1, C1, D1],
        'safe_fields': [E1, D1, C1],
        'color': WHITE
    },
    (E8,C8): {
        'rook_move': (A8, D8),
        'inner_fields': [B8, C8, D8],
        'safe_fields': [E8, D8, C8],
        'color': BLACK
    }
}




