import numpy as np
import random
from tensorflow import keras
from game.gomoku import Gomoku

class ReinforcementPlayer:
    def __init__(self, player_number, model=None):
        self.player_number = player_number
        self.model = model
        if self.model is None:
            self.build_model()

    def build_model(self):
        # Simple neural network for demonstration purposes
        input_shape = (15, 15, 3)  # Board size with 3 channels (player 1, player 2, empty)
        self.model = keras.Sequential([
            keras.layers.Input(shape=input_shape),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.Flatten(),
            keras.layers.Dense(1024, activation='relu'),
            keras.layers.Dense(15 * 15, activation='softmax')  # One output for each board position
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    def choose_move(self, game: Gomoku):
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return None

        # Prepare input for the model
        board_input = self.prepare_board_input(game)

        # Predict move probabilities
        pred = self.model.predict(np.expand_dims(board_input, axis=0))[0]

        # Zero out illegal moves
        legal_move_mask = np.zeros(15 * 15)
        for row, col in legal_moves:
            legal_move_mask[row * 15 + col] = 1

        pred = pred * legal_move_mask

        # Choose move with highest probability
        move_idx = np.argmax(pred)
        return (move_idx // 15, move_idx % 15)

    def prepare_board_input(self, game: Gomoku):
        board_input = np.zeros((15, 15, 3))
        for row in range(15):
            for col in range(15):
                if game.board[row, col] == 0:
                    board_input[row, col, 2] = 1
                elif game.board[row, col] == self.player_number:
                    board_input[row, col, 0] = 1
                else:
                    board_input[row, col, 1] = 1
        return board_input

    def play(self, game: Gomoku):
        move = self.choose_move(game)
        if move and game.make_move(*move):
            game.switch_player()

    def train(self, experiences, gamma=0.99):
        # Simple training function for demonstration purposes
        states, actions, rewards, next_states, dones = zip(*experiences)

        # Prepare inputs for the model
        states = np.array([self.prepare_board_input(state) for state in states])
        next_states = np.array([self.prepare_board_input(next_state) for next_state in next_states])

        # Predict Q-values for current states and next states
        q_values = self.model.predict(states)
        next_q_values = self.model.predict(next_states)

        # Calculate target Q-values
        targets = q_values.copy()
        for i in range(len(experiences)):
            if dones[i]:
                targets[i][actions[i]] = rewards[i]
            else:
                targets[i][actions[i]] = rewards[i] + gamma * np.max(next_q_values[i])

        # Train the model
        self.model.fit(states, targets, epochs=1, verbose=0)