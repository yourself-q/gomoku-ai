import tkinter as tk
from tkinter import ttk, messagebox
import threading
import numpy as np
from game.gomoku import Gomoku
from ai.reinforcement_player import ReinforcementPlayer
from ai.random_player import RandomPlayer

class TrainingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku AI Training")

        # Create widgets
        self.create_widgets()

        # Initialize game and players
        self.game = Gomoku()
        self.rl_player = ReinforcementPlayer(player_number=1)
        self.random_opponent = RandomPlayer(player_number=2)

    def create_widgets(self):
        # Board canvas
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack(side=tk.LEFT)

        # Control frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Start/Stop button
        self.start_button = ttk.Button(control_frame, text="Start Training", command=self.start_training)
        self.start_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(control_frame, orient='vertical', length=400, mode='determinate')
        self.progress.pack(pady=10, fill=tk.Y, expand=True)

        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready")
        self.status_label.pack(pady=10)

    def start_training(self):
        if hasattr(self, 'training_thread') and self.training_thread.is_alive():
            return  # Training already running

        self.start_button.config(state='disabled')
        self.progress['value'] = 0
        self.status_label.config(text="Training...")

        # Start training in a separate thread
        self.training_thread = threading.Thread(target=self.train_model)
        self.training_thread.start()
        self.root.after(100, self.update_progress)

    def update_progress(self):
        if hasattr(self, 'training_thread') and self.training_thread.is_alive():
            self.root.after(100, self.update_progress)
        else:
            self.progress['value'] = 100
            self.status_label.config(text="Training Complete")
            self.start_button.config(state='normal')

    def train_model(self):
        num_games = 50
        all_experiences = []

        for i in range(num_games):
            winner, experiences = self.play_game()
            all_experiences.extend(experiences)

            # Train after each game
            if isinstance(self.rl_player, ReinforcementPlayer) and experiences:
                self.rl_player.train(experiences)

            # Update progress
            progress = (i + 1) / num_games * 100
            self.progress['value'] = progress

        # Save the trained model
        self.rl_player.model.save('trained_gomoku_model.h5')

    def play_game(self):
        game = Gomoku()
        current_player = self.rl_player
        experiences = []

        while True:
            state = game.board.copy()

            # Choose and make move
            if isinstance(current_player, ReinforcementPlayer):
                action_idx = current_player.choose_move(game)
                if action_idx:
                    action = (action_idx[0] * 15 + action_idx[1],)
                    game.make_move(*action_idx)
            else:
                action = None
                move = current_player.choose_move(game)
                if move:
                    game.make_move(*move)
                    action = ((move[0] * 15 + move[1]),)

            winner = game.get_winner()

            # Record experience for the reinforcement learning player
            if isinstance(current_player, ReinforcementPlayer):
                next_state = game.board.copy() if winner == 0 and not game.is_full() else None
                done = (winner != 0) or game.is_full()
                reward = 0

                if winner == current_player.player_number:
                    reward = 1
                elif winner != 0:  # Other player won
                    reward = -1

                experiences.append((state, action, reward, next_state, done))

            if winner != 0 or game.is_full():
                return winner, experiences
            else:
                # Switch players
                current_player = self.random_opponent if current_player == self.rl_player else self.rl_player

if __name__ == "__main__":
    root = tk.Tk()
    gui = TrainingGUI(root)
    root.mainloop()