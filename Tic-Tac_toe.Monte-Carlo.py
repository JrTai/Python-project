"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 50        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.


def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player by making random moves, 
    alternating between players. The function should return when the game is over. 
    The modified board will contain the state of the game, 
    so the function does not return anything. In other words, 
    the function should modify the board input.
    """
    while board.check_win() == None:
        random_move = random.choice(board.get_empty_squares())
        board.move(random_move[0], random_move[1], player)
        player = provided.switch_player(player)
    
    
def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) 
    with the same dimensions as the Tic-Tac-Toe board, 
    a board from a completed game, and which player the machine player is. 
    The function should score the completed board and update the scores grid. 
    As the function updates the scores grid directly, it does not return anything,
    """
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == provided.PLAYERX:
                if board.check_win() == provided.PLAYERX:
                    scores[row][col] += SCORE_CURRENT
                elif board.check_win() == provided.PLAYERO:
                    scores[row][col] -= SCORE_CURRENT
            elif board.square(row, col) == provided.PLAYERO:
                if board.check_win() == provided.PLAYERO:
                    scores[row][col] += SCORE_OTHER
                elif board.check_win() == provided.PLAYERX:
                    scores[row][col] -= SCORE_OTHER
                           
def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. 
    The function should find all of the empty squares with the maximum score 
    and randomly return one of them as a (row, column) tuple. 
    It is an error to call this function with a board that has no empty squares 
    (there is no possible next move), so your function may do whatever it wants in that case. 
    The case where the board is full will not be tested.
    """
    if board.get_empty_squares() != []:
        empty_squares = board.get_empty_squares()
        
        max_score = scores[empty_squares[0][0]][empty_squares[0][1]]
        for grid in empty_squares:
            if scores[grid[0]][grid[1]] > max_score:
                max_score = scores[grid[0]][grid[1]]

        start_number = random.choice(range(len(empty_squares)))
        
        for dummy_number in range(len(empty_squares)):
            square = empty_squares[start_number]
            if scores[square[0]][square[1]] == max_score:
                return square
            start_number = (start_number + 1) % len(empty_squares)
            
    return square

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, 
    and the number of trials to run. The function should use the Monte Carlo simulation described above 
    to return a move for the machine player in the form of a (row, column) tuple. 
    Be sure to use the other functions you have written!
    """
    scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    for dummy_numbers in range(trials):
        initial = board.clone()
        mc_trial(initial, player)
        mc_update_scores(scores, initial, player)
    
    square = get_best_move(board, scores)
    return (square[0], square[1])
    
    
    

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, mc_move, NTRIALS, False)
