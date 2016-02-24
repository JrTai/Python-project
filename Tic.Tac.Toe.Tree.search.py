"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if board.check_win() != None:
        # game finish
        return SCORES[board.check_win()], (-1, -1)
    else:
        po_ls = []
        for next_move in board.get_empty_squares():
            temp_board = board.clone()
            temp_board.move(next_move[0], next_move[1], player)
            temp = mm_move(temp_board, provided.switch_player(player))
            po_ls.append((temp[0], next_move))
            if len(po_ls) == len(board.get_empty_squares()):
                if player == provided.PLAYERX:
                    return max(po_ls)
                else:
                    return min(po_ls)
    
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

#print mm_move(provided.TTTBoard(2, False, [[provided.PLAYERO, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)
#print mm_move(provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.PLAYERO, provided.PLAYERX, provided.EMPTY], [provided.EMPTY, provided.PLAYERO, provided.PLAYERX]]), provided.PLAYERX) 