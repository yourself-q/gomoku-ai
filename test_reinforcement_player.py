from game.gomoku import Gomoku
from ai.reinforcement_player import ReinforcementPlayer

g = Gomoku()
p1 = ReinforcementPlayer(1)

print('Choosing a move')
move = p1.choose_move(g)
if move:
    print(f'Chosen move: {move}')
else:
    print('No moves available')

# Test the board input preparation
board_input = p1.prepare_board_input(g)
print(f'Board input shape: {board_input.shape}')