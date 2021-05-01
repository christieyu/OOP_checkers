import sys
from board import Board
from pieces import Piece, BLACK, WHITE

class CLI:
    def __init__(self, p1="human", p2="human", history="off"):
        self.turn = 1
        self.player = WHITE
        self.white_player = sys.argv[1] if len(sys.argv) > 1 else p1
        self.black_player = sys.argv[2] if len(sys.argv) > 2 else p2
        self.history = sys.argv[3] if len(sys.argv) > 3 else history
        self.board = Board(sys.argv)

    def _display_moves(self, position):
        """Print a piece's possible moves."""
        row, col = self.board._convert_checker_coord(position)
        # Check if no piece at position
        if isinstance(self.board.board[row][col], Piece) == False:
            print("No piece at that location")
            return
        # Check if player's piece
        if self.board.board[row][col].color != self.player:
            print("That is not your piece")
            return
        # Check if no possible moves
        possible_moves = self.board._calculate_moves(position)
        if len(possible_moves) == 0:
            print("That piece cannot move")
            return
        for i, move in enumerate(possible_moves):
            print(f"{i}: {move}")
        move = input("Select a move by entering the corresponding index\n")
        self.board._execute_move(possible_moves[int(move)])
        self._new_turn()

    def _new_turn(self):
        """Checks win conditions and changes current player's turn."""
        # add something here to check for win/draw
        self.turn += 1
        self.player = BLACK if self.player == WHITE else WHITE

    def run(self):
        """Ask player for piece and display piece's possible moves."""
        while True:
            self.board._print_board()
            color = "black" if self.player == BLACK else "white"
            print(f"Turn: {self.turn}, {color}")
            player_type = self.white_player if self.player == WHITE else self.black_player
            if player_type == "human":
                position = input("Select a piece to move\n")
                self._display_moves(position)
            elif player_type == "random":
                self._random_moves(position)
            else:
                self._greedy_moves(position)