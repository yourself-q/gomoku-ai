import numpy as np
from game.gomoku import Gomoku
from ai.reinforcement_player import ReinforcementPlayer
from ai.random_player import RandomPlayer

def play_game(player1, player2):
    game = Gomoku()
    current_player = player1
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
            current_player = player2 if current_player == player1 else player1

def train_model(player, opponent, num_games=100):
    all_experiences = []

    for _ in range(num_games):
        print(f"Game {_+1}/{num_games}", end='\r')
        winner, experiences = play_game(player, opponent)
        all_experiences.extend(experiences)

        # Train after each game
        if isinstance(player, ReinforcementPlayer) and experiences:
            player.train(experiences)

    print(f"Training completed with {len(all_experiences)} experiences collected")

if __name__ == "__main__":
    # Create a reinforcement learning player and a random opponent
    rl_player = ReinforcementPlayer(player_number=1)
    random_opponent = RandomPlayer(player_number=2)

    # Train the model
    train_model(rl_player, random_opponent, num_games=50)

    # Save the trained model
    rl_player.model.save('trained_gomoku_model.h5')