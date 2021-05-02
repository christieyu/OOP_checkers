# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

import sys
import random
import copy
from board import Board
from players import PlayerState, WhiteState, BlackState, PlayerMove
from pieces import Piece
from moves import Move, Jump, Simple


class CLI:
    def __init__(self, p1="human", p2="human"):
        self.turn = 1
        self.white_state = WhiteState(self, sys.argv[1] if len(sys.argv) > 1 else p1)
        self.black_state = BlackState(self, sys.argv[2] if len(sys.argv) > 2 else p2)
        self.player_state = self.white_state
        self.history = True if len(sys.argv) > 3 else False
        self.move_history = []
        self.board = Board(sys.argv)
        # strategy pattern setup
        self._choices = {
            "human": self._human_moves,
            "random": self._random_moves,
            "greedy": self._greedy_moves,
        }
        self._update_moveset()
        # get randomized seed
        with open('seed.txt', 'r') as seed_f:
            seed_value = seed_f.read()
        random.seed(seed_value)

    def _toggle_color(self):
        self.player_state._toggle_color()

    def _human_moves(self):
        """Print a piece's possible moves."""
        position = input("Select a piece to move\n")
        row, col = self.board._convert_checker_coord(position)
        # Check if no piece at position
        if isinstance(self.board.board[row][col], Piece) == False:
            print("No piece at that location")
            return
        # Check if player's piece
        if self.board.board[row][col].color != self.player_state.color:
            print("That is not your piece")
            return
        # Check if no possible moves or possible jumps not selected
        possible_moves = self.board._calculate_moves(position)
        if len(possible_moves) == 0 or (isinstance(possible_moves[0], Simple) and True in [isinstance(move, Jump) for move in self.player_state.moves]):
            print("That piece cannot move")
            return
        # Otherwise move is valid
        for i, move in enumerate(possible_moves):
            print(f"{i}: {move}")
        choice = input("Select a move by entering the corresponding index\n")

        # move_obj = possible_moves[int(choice)]
        move = PlayerMove(self.turn, self.player_state, possible_moves[int(choice)], copy.deepcopy(self.board))
        self.move_history.append(move)
        move.execute(self.board)


    def _random_moves(self):
        # choose a random move from moveset but prioritize jumps
        jump_moves = [move for move in self.player_state.moves if isinstance(move, Jump)]
        if len(jump_moves) > 0:
            move = random.choice(jump_moves)
        else:
            move = random.choice(self.player_state.moves)
        move = PlayerMove(self.turn, self.player_state, move, copy.deepcopy(self.board))
        self.move_history.append(move)
        move.execute(self.board)

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
        move = PlayerMove(self.turn, self.player_state, move, copy.deepcopy(self.board))
        self.move_history.append(move)
        move.execute(self.board)


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

    def _do_history(self):
        """Presents undo/redo/next options at beginning of turn. Returns False if history is disable or "next"
        is selected, otherwise returns True (skipping usual move operations for undo/redo)"""
        if not self.history:
            return False
        op = input("undo, redo, or next\n")
        try:
            if op == "undo":
                self.turn -= 1
                last_move = self.move_history[self.turn - 1]
                self.board = copy.deepcopy(last_move.board_state)
                self.player_state = last_move.player_state
                return True
            elif op == "redo":
                next_move = self.move_history[self.turn - 1]
                next_move.execute(self.board)
                self.turn += 1
                self.player_state._toggle_color()
                return True
        except IndexError:
            return True                                                 # if undo/redo unavailable, don't do anything
        
        self.move_history = self.move_history[:self.turn-1]             # if new history branch, cut off old paths
        return False

    def _check_victory_draw(self):
        """Checks win conditions and changes current player's turn."""
        # victory conditions
        if self.player_state.pieces_left == False:
            self.player_state._toggle_color()
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
            if self._do_history():
                continue
            self._choices.get(self.player_state.player)()
            self._new_turn()