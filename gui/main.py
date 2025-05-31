import tkinter as tk
from tkinter import messagebox
from game.gomoku import Gomoku

class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku Game")

        self.game = Gomoku()
        self.board_size = self.game.board_size
        self.cell_size = 40

        self.canvas = tk.Canvas(root,
                               width=self.board_size * self.cell_size,
                               height=self.board_size * self.cell_size)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.draw_board()
        self.update_board()

    def draw_board(self):
        for i in range(self.board_size):
            # Draw horizontal lines
            self.canvas.create_line(0, i * self.cell_size,
                                   self.board_size * self.cell_size,
                                   i * self.cell_size)
            # Draw vertical lines
            self.canvas.create_line(i * self.cell_size, 0,
                                   i * self.cell_size,
                                   self.board_size * self.cell_size)

    def update_board(self):
        self.canvas.delete("pieces")
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.game.board[row, col] == 1:
                    self.canvas.create_oval(col * self.cell_size + 5,
                                            row * self.cell_size + 5,
                                            (col + 1) * self.cell_size - 5,
                                            (row + 1) * self.cell_size - 5,
                                            fill="black", tags="pieces")
                elif self.game.board[row, col] == 2:
                    self.canvas.create_oval(col * self.cell_size + 5,
                                            row * self.cell_size + 5,
                                            (col + 1) * self.cell_size - 5,
                                            (row + 1) * self.cell_size - 5,
                                            fill="white", tags="pieces")

    def on_canvas_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.game.make_move(row, col):
            winner = self.game.get_winner()
            if winner != 0:
                messagebox.showinfo("Game Over", f"Player {winner} wins!")
                self.game.reset()
                self.update_board()
            else:
                self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    gui = GomokuGUI(root)
    root.mainloop()