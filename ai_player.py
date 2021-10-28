# Functions to build an AI Tic Tac Toe player. Inspiration from a project I completed for
# the Harvard ai50 course.

import math
import copy
import random

X = "X"
O = "O"
EMPTY = None

# Checks the board to see whose turn it is. X always has the first turn
def player(board):
	x = 0
	o = 0
	for row in board:
		for col in row:
			if col == X:
				x += 1
			elif col == O:
				o += 1
	if x == o:
		return X
	else:
		return O

# Return all the possible actions as a set of tuples (i, j) where i corresponds to the 
# row number and j to the cell on the row. Possible actions are all empty slots on
# the board.
def actions(board):
	actions_list = set()
	i = 0
	while i < len(board):
		j = 0
		while j < len(board[i]):
			if board[i][j] == EMPTY:
				pair = (i, j)
				actions_list.add(pair)
			j += 1
		i += 1
	return actions_list

# Makes a deep copy of the board and places the action (move)(i, j) on it.
def result(board, action):
	copy_board = copy.deepcopy(board)
	next_player = player(board)
	if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2 or copy_board[action[0]][action[1]] != EMPTY:
		raise NotImplementedError
	copy_board[action[0]][action[1]] = next_player
	return copy_board
	

# Return the winner if there is one, otherwise returns None
def winner(board):

	#check rows
	for row in board:
		if row[0] != EMPTY and all(row[0] == elem for elem in row):
			return row[0]
	#check columns
	for j in range(3):
		if all(board[0][j] == elem for elem in [board[0][j], board[1][j], board[2][j]]) and board[0][j] != EMPTY:
			return board[0][j]
	#check diagonal
	if (all(board[1][1] == elem for elem in [board[0][0], board[2][2]]) or 
		all(board[1][1] == elem for elem in [board[0][2], board[2][0]])) and board[1][1] != EMPTY:
		return board[1][1]
	#else it's a tie
	return None

# Checks to see if the game is over, in which case returns True
def terminal(board):

	actions_list = actions(board)
	if len(actions_list) == 0 or winner(board):
		return True
	else:
		return False


# Return 1 if X has won, -1 if O has won, 0 otherwise
def utility(board):
	game_winner = winner(board)
	if not game_winner:
		return 0
	if game_winner == X:
		return 1
	else:
		return -1


def maxim_value(board):
	val = -math.inf
	if terminal(board):
		return utility(board)
	try_actions = actions(board)
	for action in try_actions:
		val = max(val, minim_value(result(board, action)))
	return val

def minim_value(board):
	val = math.inf
	if terminal(board):
		return utility(board)
	try_actions = actions(board)
	for action in try_actions:
		val = min(val, maxim_value(result(board, action)))
	return val


# Returns the optimal move for the current player on the board. Goes through each possible
# move and deepdives to minim_value() or maxim_value() depending if the current player is the 
# maximizing player (X). Then alternates recursively between maxim_value() and minim_value()
# pretending to be the opponent. minim_value() and maxim_value() return -1, 0 or 1 depending on 
# who won the game in that one simulation. Ultimately, minimax() will save the value and the move
# that is most favorable for the current player. If multiple moves result in the same (best) outcome,
# the first one simulated will be returned.
def minimax(board):

	if terminal(board):
		return None

	actions_list = actions(board)
	pl = player(board)
	init_value = -math.inf if pl == X else math.inf
	best_action = None

	#For faster execution, check if AI is X player playing their first move.
	# in this case, pick random action
	if pl == X and all([EMPTY, EMPTY, EMPTY] == elem for elem in board):
		return random.choice(list(actions_list))

	for action in actions_list:
		if pl == X:
			ret_val = minim_value(result(board, action))
			if ret_val > init_value:
				init_value = ret_val
				best_action = action

		else:
			ret_val = maxim_value(result(board, action))
			if ret_val < init_value:
				init_value = ret_val
				best_action = action

	return best_action
