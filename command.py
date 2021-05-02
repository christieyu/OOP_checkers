# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

import sys
import random
from board import Board
from players import PlayerState, WhiteState, BlackState
from pieces import Piece

class CLI:
    def __init__(self, p1="human", p2="human", history="off"):
        self.turn = 1
        self.white_state = WhiteState(self, sys.argv[1] if len(sys.argv) > 1 else p1)
        self.black_state = BlackState(self, sys.argv[2] if len(sys.argv) > 2 else p2)
        self.player_state = self.white_state
        self.history = sys.argv[3] if len(sys.argv) > 3 else history
        self.board = Board(sys.argv)
        self._update_moveset()
        # get randomized seed
        with open('seed.txt', 'r') as seed_f:
            seed_value = seed_f.read()
        random.seed(seed_value)

    def _toggle_color(self):
        self.player_state._toggle_color()

    def _human_moves(self, position):
        """Print a piece's possible moves."""
        row, col = self.board._convert_checker_coord(position)
        # Check if no piece at position
        if isinstance(self.board.board[row][col], Piece) == False:
            print("No piece at that location")
            return
        # Check if player's piece
        if self.board.board[row][col].color != self.player_state.color:
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
        move = random.choice(self.player_state.moves)
        self.board._execute_move(move)

    def _greedy_moves(self):
        # go through board for valid pieces with possible moves and find greediest moveset
        greedy_move_length = -1
        greedy_move_choices = []
        for move in self.player_state.moves:
            if len(move.eliminated) > greedy_move_length:
                greedy_move_length = len(move.eliminated)
                greedy_move_choices = [move]
            elif len(move.eliminated) == greedy_move_length:
                greedy_move_choices.append(move)
        # choose a random move from list
        move = random.choice(greedy_move_choices)
        self.board._execute_move(move)

    def _update_moveset(self):
        # check win condition by assessing all possible moves of current player
        total_moves = []
        self.player_state.pieces_left = False
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                if isinstance(self.board.board[row][col], Piece) and self.board.board[row][col].color == self.player_state.color:
                    self.player_state.pieces_left = True
                    possible_moves = self.board._calculate_moves((row, col), True)
                    if len(possible_moves) > 0:
                        for move in possible_moves:
                            total_moves.append(move)
        self.player_state.moves = total_moves

    def _new_turn(self):
        # game continues
        self.turn += 1
        self.player_state._toggle_color()
        self._update_moveset()

    def _check_victory_draw(self):
        """Checks win conditions and changes current player's turn."""
        # victory conditions
        if self.player_state.pieces_left == False:
            print(f"{self.player_state} has won")
            sys.exit(0)
        # draw conditions
        elif len(self.player_state.moves) == 0:
            print("draw")
            sys.exit(0)
        if self.board.draw_counter >= 50:
            print("draw")
            sys.exit(0)

    def run(self):
        """Ask player for piece and display piece's possible moves."""
        while True:
            self.board._print_board()
            print(f"Turn: {self.turn}, {self.player_state}")
            self._check_victory_draw()
            if self.player_state.player == "human":
                position = input("Select a piece to move\n")
                self._human_moves(position)
            elif self.player_state.player == "random":
                self._random_moves()
            else:
                self._greedy_moves()
            self._new_turn()