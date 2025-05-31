import numpy as np

class Gomoku:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = 1  # Player 1 starts (black)

    def reset(self):
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1

    def make_move(self, row, col):
        if self.board[row, col] == 0:
            self.board[row, col] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = 3 - self.current_player  # Switch between 1 and 2

    def get_winner(self):
        # Check horizontal, vertical, and diagonal lines for a winner
        for i in range(self.board_size):
            for j in range(self.board_size - 4):
                if abs(np.sum(self.board[i, j:j+5])) == 5:
                    return np.sign(np.sum(self.board[i, j:j+5]))

            for j in range(self.board_size - 4):
                if abs(np.sum(self.board[j:j+5, i])) == 5:
                    return np.sign(np.sum(self.board[j:j+5, i]))

        for i in range(self.board_size - 4):
            for j in range(self.board_size - 4):
                if abs(np.sum(np.diag(self.board, k=i-j)[i:i+5])) == 5:
                    return np.sign(np.sum(np.diag(self.board, k=i-j)[i:i+5]))

                if abs(np.sum(np.diag(np.fliplr(self.board), k=i-j)[i:i+5])) == 5:
                    return np.sign(np.sum(np.diag(np.fliplr(self.board), k=i-j)[i:i+5]))

        return 0  # No winner

    def is_full(self):
        return np.all(self.board != 0)

    def get_legal_moves(self):
        return list(zip(*np.where(self.board == 0)))

    def print_board(self):
        for row in self.board:
            print(' '.join(['•' if cell == 0 else ('●' if cell == 1 else '○') for cell in row]))