import sys
from board import Board

class CLI:

    def __init__(self, argv=sys.argv):
        self.turn = 0
        self.player = "white"
        if len(sys.argv) == 0:
            self.board = Board()
        elif len(sys.argv) == 1:
            self.board = Board(sys.argv[0])
        elif len(sys.argv) == 2:
            self.board = Board(sys.argv[0], sys.argv[1])
        else:
            self.board = Board(sys.argv[0], sys.argv[1], sys.argv[2])

    def _display_moves(self, piece):
        """Print a piece's possible moves."""
        # TODO
        print(f"0: MOVE 0")
        print(f"1: MOVE 1")
        print(f"2: MOVE 2")

    def run(self):        
        """Ask player for piece and display piece's possible moves."""
        while True:
            self.board._print_board()
            print(f"Turn: {self.turn}, {self.player}")
            piece = input("Select a piece to move\n")
            self._display_moves(piece)