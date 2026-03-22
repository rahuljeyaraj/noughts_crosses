from modules.board import Board
from modules.player import Player

board = Board()
p1 = Player(name="Alice", symbol="X")
p2 = Player(name="Bob", symbol="O")

board.place_mark(0, p1.symbol)
board.place_mark(4, p2.symbol)
board.place_mark(1, p1.symbol)
board.place_mark(3, p2.symbol)
board.place_mark(2, p1.symbol)

print(board.render())
print(board.check_winner())
print(board.get_winning_line())

p1.record_win()
p2.record_loss()
print(p1.score_summary())
