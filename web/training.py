from flask import Flask, render_template, jsonify
import threading
import time
import sys
sys.path.append('/workspace')
from ai.reinforcement_player import ReinforcementPlayer
from ai.random_player import RandomPlayer

app = Flask(__name__)
training_thread = None
training_data = {
    'status': 'ready',
    'progress': 0,
    'wins': 0,
    'losses': 0,
    'draws': 0
}

def train_model():
    global training_data
    training_data['status'] = 'training'
    training_data['progress'] = 0

    rl_player = ReinforcementPlayer(player_number=1)
    random_opponent = RandomPlayer(player_number=2)

    num_games = 50
    all_experiences = []

    for i in range(num_games):
        winner, experiences = play_game(rl_player, random_opponent)
        all_experiences.extend(experiences)

        # Train after each game
        if isinstance(rl_player, ReinforcementPlayer) and experiences:
            rl_player.train(experiences)

        # Update training data
        training_data['progress'] = (i + 1) / num_games * 100

        if winner == 1:
            training_data['wins'] += 1
        elif winner == 2:
            training_data['losses'] += 1
        else:
            training_data['draws'] += 1

    # Save the trained model
    rl_player.model.save('trained_gomoku_model.h5')

    training_data['status'] = 'complete'

def play_game(player1, player2):
    from game.gomoku import Gomoku
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

@app.route('/')
def index():
    return render_template('training.html')

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(training_data)

@app.route('/train', methods=['POST'])
def start_training():
    global training_thread, training_data
    if training_thread and training_thread.is_alive():
        return jsonify({'error': 'Training already in progress'})

    training_data = {
        'status': 'ready',
        'progress': 0,
        'wins': 0,
        'losses': 0,
        'draws': 0
    }

    training_thread = threading.Thread(target=train_model)
    training_thread.start()

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52843, debug=True)  # Changed to a different port