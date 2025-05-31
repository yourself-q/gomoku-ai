import random
from game.gomoku import Gomoku
from ai.random_player import RandomPlayer

def play_game(player1, player2):
    game = Gomoku()
    current_player = player1

    while True:
        current_player.play(game)
        winner = game.get_winner()

        if winner != 0:
            return winner
        elif game.is_full():
            return 0  # Draw

        # Switch players
        current_player = player2 if current_player == player1 else player1

def train_models(player1, player2, num_games=100):
    results = {'player1': 0, 'player2': 0, 'draws': 0}

    for _ in range(num_games):
        winner = play_game(player1, player2)
        if winner == 1:
            results['player1'] += 1
        elif winner == 2:
            results['player2'] += 1
        else:
            results['draws'] += 1

    return results

if __name__ == "__main__":
    player1 = RandomPlayer(1)
    player2 = RandomPlayer(2)

    results = train_models(player1, player2, num_games=100)
    print(f"Training Results: {results}")