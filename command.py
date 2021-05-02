import sys
import random
from board import Board
from pieces import Piece, BLACK, WHITE

class CLI:
    def __init__(self, p1="human", p2="human", history="off"):
        self.turn = 1
        self.player = WHITE
        self.white_player = sys.argv[1] if len(sys.argv) > 1 else p1
        self.white_moves = []
        self.black_player = sys.argv[2] if len(sys.argv) > 2 else p2
        self.black_moves = []
        self.history = sys.argv[3] if len(sys.argv) > 3 else history
        self.board = Board(sys.argv)
        self._update_moveset(WHITE)
        self._update_moveset(BLACK)
        # get randomized seed
        with open('seed.txt', 'r') as seed_f:
            seed_value = seed_f.read()
        random.seed(seed_value)

    def _human_moves(self, position):
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
        # Otherwise move is valid
        for i, move in enumerate(possible_moves):
            print(f"{i}: {move}")
        move = input("Select a move by entering the corresponding index\n")
        self.board._execute_move(possible_moves[int(move)])

    def _random_moves(self):
        # choose a random move from moveset
        move = random.choice(self.white_moves) if self.player == WHITE else random.choice(self.black_moves)
        self.board._execute_move(move)

    def _greedy_moves(self):
        # go through board for valid pieces with possible moves and find greediest moveset
        greedy_move_length = -1
        greedy_move_choices = []
        moveset = self.white_moves if self.player == WHITE else self.black_moves
        for move in moveset:
            if len(move.eliminated) > greedy_move_length:
                greedy_move_length = len(move.eliminated)
                greedy_move_choices = [move]
            elif len(move.eliminated) == greedy_move_length:
                greedy_move_choices.append(move)
        # choose a random move from list
        move = random.choice(greedy_move_choices)
        self.board._execute_move(move)

    def _update_moveset(self, color):
        # check win condition by assessing all possible moves of current player
        total_moves = []
        if color == WHITE:
            self.white_pieces_left = False
        else:
            self.black_pieces_left = False
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                if isinstance(self.board.board[row][col], Piece) and self.board.board[row][col].color == color:
                    if color == WHITE:
                        self.white_pieces_left = True
                    else:
                        self.black_pieces_left = True
                    possible_moves = self.board._calculate_moves((row, col), True)
                    if len(possible_moves) > 0:
                        for move in possible_moves:
                            total_moves.append(move)
        if color == BLACK:
            self.black_moves = total_moves
        else:
            self.white_moves = total_moves

    def _new_turn(self):
        # game continues
        self.turn += 1
        self.player = BLACK if self.player == WHITE else WHITE
        self._update_moveset(self.player)

    def _check_victory_draw(self):
        """Checks win conditions and changes current player's turn."""
        # victory conditions
        moves_left = self.white_moves if self.player == WHITE else self.black_moves
        if (self.white_pieces_left == False and self.player == WHITE) or (self.black_pieces_left == False and self.player == BLACK):
            color = "black" if self.player == BLACK else "white"
            print(f"{color} has won")
            sys.exit(0)
        # draw conditions
        elif len(moves_left) == 0:
            print("draw")
            sys.exit(0)
        if self.board.draw_counter >= 50:
            print("draw")
            sys.exit(0)

    def run(self):
        """Ask player for piece and display piece's possible moves."""
        while True:
            self.board._print_board()
            color = "black" if self.player == BLACK else "white"
            print(f"Turn: {self.turn}, {color}")
            self._check_victory_draw()
            player_type = self.white_player if self.player == WHITE else self.black_player
            if player_type == "human":
                position = input("Select a piece to move\n")
                self._human_moves(position)
            elif player_type == "random":
                self._random_moves()
            else:
                self._greedy_moves()
            self._new_turn()