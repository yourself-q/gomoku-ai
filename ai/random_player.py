import random
from game.gomoku import Gomoku

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number

    def choose_move(self, game: Gomoku):
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return None
        return random.choice(legal_moves)

    def play(self, game: Gomoku):
        move = self.choose_move(game)
        if move:
            game.make_move(*move)
            game.switch_player()