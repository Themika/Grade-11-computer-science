import random

class TicTacToeAI:
    # Initialize the AI with the symbol it will use
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = "O" if symbol == "X" else "X"

    def get_move(self, board, difficulty):
        # Get the move based on the difficulty
        if difficulty == "easy":
            return self.random_move(board)
        elif difficulty == "medium":
            return self.medium_move(board)
        elif difficulty == "hard":
            return self.minimax_move(board)

    def random_move(self, board):
        # Easy difficulty: Random move
        empty_cells = [(i, j) for i in range(len(board)) for j in range(len(board[i])) if board[i][j] == ""]
        return random.choice(empty_cells)

    def medium_move(self, board):
        # Medium difficulty: Random move with a chance to block the player
        move = self.random_move(board)
        # Check if the AI can win
        if random.random() < 0.5:
            return move
        # Check if the player can win
        return self.minimax_move(board)

    def minimax_move(self, board):
        # Hard difficulty: Minimax algorithm
        best_score = float('-inf')
        best_move = None
        # Loop through all the empty cells
        for i in range(len(board)):
            for j in range(len(board[i])):
                # Check if the cell is empty
                if board[i][j] == "":
                    board[i][j] = self.symbol
                    score = self.minimax(board, 0, False)
                    board[i][j] = ""
                    # Update the best move
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        # Return the best move
        return best_move

    def minimax(self, board, depth, is_maximizing):
        # Check if the game is over
        winner = self.check_winner(board)
        # Return the score based on the winner
        if winner == self.symbol:
            return 1
        elif winner == self.opponent_symbol:
            return -1
        elif winner == "Tie":
            return 0
        # Check if the AI is maximizing or minimizing
        if is_maximizing:
            # Maximizing
            best_score = float('-inf')
            # Loop through all the empty cells
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == "":
                        board[i][j] = self.symbol
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best_score = max(score, best_score)
            # Return the best score
            return best_score
        else:
            # Minimizing
            best_score = float('inf')
            # Loop through all the empty cells
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == "":
                        board[i][j] = self.opponent_symbol
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best_score = min(score, best_score)
            # Return the best score
            return best_score

    def check_winner(self, board):
        # Check if there is a winner
        size = len(board)
        win_length = 3
        # Check rows
        for row in board:
            for i in range(size - win_length + 1):
                if all(cell == row[i] != '' for cell in row[i:i+win_length]):
                    return row[i]
        # Check columns
        for col in range(size):
            for i in range(size - win_length + 1):
                if all(board[row][col] == board[i][col] != '' for row in range(i, i+win_length)):
                    return board[i][col]
        # Check diagonals
        for i in range(size - win_length + 1):
            for j in range(size - win_length + 1):
                if all(board[i+k][j+k] == board[i][j] != '' for k in range(win_length)):
                    return board[i][j]
                if all(board[i+k][j+win_length-1-k] == board[i][j+win_length-1] != '' for k in range(win_length)):
                    return board[i][j+win_length-1]
        # Check for a tie
        if all(board[i][j] != '' for i in range(size) for j in range(size)):
            return 'Tie'
        return None