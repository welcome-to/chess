from board import Figure, Move, Coordinates, figures_on_board
from const import *
from exception import InternalError, InvalidMove
from fucking_cord_const import *
from common_operations import another_color, is_pawn_jump, create_move







def is_e_p_correct(board, start, end, prev_move, player_color):
    figure = board.figure_on_position(start)
    if figure.type != PAWN or figure.color != player_color:
        return False
    if not is_pawn_jump(board, prev_move, another_color(player_color)):
        return False
    if abs(prev_move.start.x - start.x) != 1 or \
       prev_move.start.y - end.y != end.y - prev_move.end.y or \
       abs(prev_move.start.y - end.y) != 1 or \
       prev_move.start.x != end.x:

       return False
    return True


def possible_e_p_from_position(board, position, player_color, previous_move):
    if not previous_move or not position.y in [3, 4] or not is_pawn_jump(board, previous_move, another_color(player_color)):
        return []

    final_pos = list(filter(
        lambda end: is_e_p_correct(board, position, end, previous_move, player_color),
        filter(bool, [
            position.top_left(), position.top_right(),
            position.bottom_left(), position.bottom_right()
        ])
    ))
    ans = []
    for pos in final_pos:
        ans.append(create_move(position, pos, board, player_color))
    return ans
    

