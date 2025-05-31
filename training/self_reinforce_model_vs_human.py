import numpy as np
from game.gomoku import Gomoku
from ai.reinforcement_player import ReinforcementPlayer

def play_game(player, human_player_number):
    game = Gomoku()
    current_player = player if player.player_number != human_player_number else None

    while True:
        if current_player is None:  # Human's turn - we'll just simulate
            legal_moves = game.get_legal_moves()
            if not legal_moves:
                break
            move = legal_moves[np.random.randint(len(legal_moves))]
            game.make_move(*move)
        else:
            action_idx = current_player.choose_move(game)
            if action_idx and game.make_move(*action_idx):
                pass

        winner = game.get_winner()
        if winner != 0 or game.is_full():
            break

        # Switch players
        current_player = player if current_player is None else None

    return winner, []

def collect_human_data(player, human_player_number, num_games=10):
    all_experiences = []

    for i in range(num_games):
        print(f"Game {i+1}/{num_games}", end='\r')
        winner, experiences = play_game(player, human_player_number)
        all_experiences.extend(experiences)

    print(f"Data collection completed with {len(all_experiences)} experiences collected")
    return all_experiences

def train_model(player, experiences):
    if isinstance(player, ReinforcementPlayer) and experiences:
        player.train(experiences)

if __name__ == "__main__":
    # Create a reinforcement learning player
    player = ReinforcementPlayer(player_number=2)  # Player 2 (white)

    # Load pre-trained model if available
    try:
        player.model = keras.models.load_model('trained_gomoku_model.h5')
    except:
        print("Using untrained reinforcement learning player")

    # Collect data from playing against a human-like player
    experiences = collect_human_data(player, human_player_number=1, num_games=50)

    # Train the model with collected data
    train_model(player, experiences)

    # Save the trained model
    player.model.save('trained_gomoku_model.h5')