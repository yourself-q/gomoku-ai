from game.gomoku import Gomoku

def fight(player1, player2):
    """
    Make two players (models) play against each other.

    Args:
        player1: First player object with a 'play' method
        player2: Second player object with a 'play' method

    Returns:
        Winner (1 or 2) or 0 for draw
    """
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

if __name__ == "__main__":
    from ai.random_player import RandomPlayer
    from ai.reinforcement_player import ReinforcementPlayer

    # Load a pre-trained model (if available)
    try:
        rl_player = ReinforcementPlayer(player_number=1)
        rl_player.model = keras.models.load_model('trained_gomoku_model.h5')
    except:
        print("Using untrained reinforcement learning player")
        rl_player = ReinforcementPlayer(player_number=1)

    random_player = RandomPlayer(player_number=2)

    # Play a game
    winner = fight(rl_player, random_player)
    if winner == 0:
        print("The game ended in a draw")
    else:
        print(f"Player {winner} wins!")