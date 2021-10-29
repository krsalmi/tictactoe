# Tic Tac Toe game program that prints moves on stdout

import ai_player as ai
import time

EMPTY = None
X = "X"
O = "O"
MODE = None
PL_1 = None
PL_2 = None

# Defines game mode from users input and saves the mode into a global variable
def define_game_mode():
	print("This is the classic game Tic Tac Toe, which can be played in the following 3 ways:")
	print("1 = two people")
	print("2 = person vs AI player")
	print("3 = two AI players")
	print("Enter number 1, 2 or 3 according to the type of Tic Tac Toe mode you want")
	mode = input()
	while not mode.isdigit() or not 1 <= int(mode) <= 3:
		mode = input("Must be 1, 2 or 3\n")
	global MODE
	MODE = int(mode)

# Defines which player plays x and which o. Prints instructions
def define_players_print_instructions():
	if MODE == 1 or MODE == 2:
		pl_1 = input("Player 1, enter X or O to choose your sign\n")
		while pl_1.upper() != 'X' and pl_1.upper() != 'O':
			pl_1 = input("Enter X or O\n")
		global PL_1
		PL_1 = pl_1.upper()
		global PL_2
		PL_2 = 'O' if PL_1 == 'X' else 'X'
		print("\nPlayer 1 will play " + PL_1)
		if MODE == 2:
			print("Player 2 (AI player) will play " + PL_2)
		else:
			print("Player 2 will play " + PL_2)
		print("\nThe game board will be represented by a 3 x 3 grid, each slot having a corresponding number:")
		print("\n| 1 | 2 | 3 |\n| 4 | 5 | 6 |\n| 7 | 8 | 9 |\n")
		print("Human players will be asked to enter the number of the slot they've chosen")
		print("The player who plays 'X' gets the first turn")
	else:
		PL_1 = 'X'
		PL_2 = 'O'
		print("Selected game mode = 3, two AI players competing")

# Initial, empty board
def empty_board():
	return [[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY]]

def print_turn(player):
	print("\nPlayer 1's" if player == PL_1 else "\nPlayer 2's", end=" ")
	print("(" + player + ") turn to play")

# Prompt the human player for a move by asking for a number. If given input is not a number,
# or number is not between 1 and 9, or if that slot is not empty, the player will be prompted again
def get_human_move(next_player, board):
	print("\nPlayer number 1, " if next_player == PL_1 else "\nPlayer number 2, ", end="")
	slot = input("enter number of the slot you want to place your '" + next_player + "' in\n")
	while True:
		while not slot.isdigit() or not 1 <= int(slot) <= 9:
			slot = input("Must be a number between 1 and 9\n")
		row = (int(slot) - 1) // 3
		col = (int(slot) - 1) % 3
		if board[row][col] != EMPTY:
			slot = input("Chosen slot is not empty, choose another one\n")
		else:
			break
	return (row, col)

# Handles a round of the game by first determining and printing whose turn it is, printing
# the board and then executing the chosen move. If it is the turn of an AI player, the move
# will result from calling minimax(). Otherwise the human player will be prompted for their
# chosen move in get_human_move()
def run_game(board):
	next_player = ai.player(board)
	print_turn(next_player)
	print_board(board)
	if MODE == 3 or (MODE ==2 and next_player != PL_1):
		time.sleep(1)
		move = ai.minimax(board)
	else:
		move = get_human_move(next_player, board)
	board[move[0]][move[1]] = next_player

# Prints the game board	
def print_board(board):
	for row in board:
		for slot in row:
			print("|", end="")
			print(" " if slot == EMPTY else slot, end="")
		print("|")

def main():
	define_game_mode()
	define_players_print_instructions()
	board = empty_board()
	while not ai.terminal(board):
		run_game(board)
	if ai.terminal(board):
		print("\nGAME OVER!")
		print_board(board)
		winner = ai.winner(board)
		if not winner:
			print("\nDraw, no one wins!")
		else:
			print("\nPlayer 1" if winner == X else "\nPlayer 2", end=" ")
			print("("+ winner +")", "wins!")
		

if __name__ == "__main__":
	main()