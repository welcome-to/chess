from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove
from fucking_cord_const import *
from common_operations import another_color
from common_moves import possible_common_moves_from_position

from functools import reduce


def fields_under_attack(board, enemy_color):
    attacked = [possible_common_moves_from_position(board, item[1], enemy_color) for item in figures_on_board(board, color=enemy_color)] 
    # FIXME: e_p_moves
    return reduce(lambda x,y: set(x) | set(y), attacked, set())


def is_castling_correct(king_move, board, player_color):
    assert(king_move.type == CASTLING_MOVE)

    castling_data = CASTLING_DATA[(king_move.start,king_move.end)]
    rook_move = king_move.extra_move
    assert(rook_move is not None)

    king = board.figure_on_position(king_move.start)
    assert(king is not None)
    if king.color != player_color or king.color != CASTLING_DATA[(king_move.start,king_move.end)]['color']:
        return False

    rook = board.figure_on_position(rook_move.start)
    if rook is None or rook.color != player_color or rook.color != CASTLING_DATA[(king_move.start,king_move.end)]['color']:
        return False

    if king.has_moved or rook.has_moved:
        return False

    # no figures between king and rook
    for inner_field in castling_data['inner_fields']:
        if not board.figure_on_position(inner_field) is None:
            return False

    # 3. Check the king's way is not under attack.
    under_attack = fields_under_attack(board, another_color(player_color))
    if set(castling_data['safe_fields']) & set(under_attack):
        return False

    return True




