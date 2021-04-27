import sys
from board import Board

class CLI:
    def __init__(self, argv=sys.argv):
        self.turn = 0
        self.player = "white"
        self.board = Board(sys.argv)

    def _display_moves(self, position):
        """Print a piece's possible moves."""
        possible_moves = self.board._calculate_moves(position)
        for i, move in enumerate(possible_moves):
            if move.type == "simple":
                print(f"{i}: basic move: {position}->{move.end}")
        move = input("Select a move by entering the corresponding index\n")
        self.board._execute_move(possible_moves[int(move)])

    def run(self):
        """Ask player for piece and display piece's possible moves."""
        while True:
            self.board._print_board()
            print(f"Turn: {self.turn}, {self.player}")
            position = input("Select a piece to move\n")
            self._display_moves(position)
            self.turn += 1
            if self.player == "white":
                self.player = "black"
            else:
                self.player == "white"