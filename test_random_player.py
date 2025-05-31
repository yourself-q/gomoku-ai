from game.gomoku import Gomoku
from ai.random_player import RandomPlayer

g = Gomoku()
p1 = RandomPlayer(1)
p2 = RandomPlayer(2)

print('Playing random moves')
for _ in range(5):
    p1.play(g)
    if g.get_winner() != 0:
        break
    p2.play(g)
    if g.get_winner() != 0:
        break

print('Winner:', g.get_winner())
g.print_board()