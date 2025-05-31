from flask import Flask, render_template, jsonify, request
import numpy as np
import sys
sys.path.append('/workspace')
from game.gomoku import Gomoku

app = Flask(__name__)
game = Gomoku()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/board', methods=['GET'])
def get_board():
    board_data = game.board.tolist()
    current_player = game.current_player
    winner = game.get_winner()
    return jsonify({
        'board': board_data,
        'currentPlayer': current_player,
        'winner': winner
    })

@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    row, col = data['row'], data['col']

    if game.make_move(row, col):
        winner = game.get_winner()
        return jsonify({'success': True, 'winner': winner})
    else:
        return jsonify({'success': False})

@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=59879, debug=True)  # Changed to a different port