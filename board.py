# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

from pieces import Piece, Pawn, King
import moves

class Board:
    def __init__(self, p1="human", p2="human", history="off"):
        """Initialize board where 0 is an unplayable space and 1 is a playable space."""

        # this is the standard starting layout! wowzers!
        # (ok yeah this looks terrible I'm sorry maybe we can change later? idk)
        self.board = [[Pawn("black", (0, 0)), 0, Pawn("black", (0, 2)), 0, Pawn("black", (0, 4)), 0, Pawn("black", (0, 6)), 0],
                      [0, Pawn("black", (1, 1)), 0, Pawn("black", (1, 3)), 0, Pawn("black", (1, 5)), 0, Pawn("black", (1, 7))],
                      [Pawn("black", (2, 0)), 0, Pawn("black", (2, 2)), 0, Pawn("black", (2, 4)), 0, Pawn("black", (2, 6)), 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, Pawn("white", (5, 1)), 0, Pawn("white", (5, 3)), 0, Pawn("white", (5, 5)), 0, Pawn("white", (5, 7))],
                      [Pawn("white", (6, 0)), 0, Pawn("white", (6, 2)), 0, Pawn("white", (6, 4)), 0, Pawn("white", (6, 6)), 0],
                      [0, Pawn("white", (7, 1)), 0, Pawn("white", (7, 3)), 0, Pawn("white", (7, 5)), 0, Pawn("white", (7, 7))]]

        # lookie here! it's a modified board for looking at jumps! wowzers!
        # self.board = [[Pawn("black", (0, 0)), 0, 1, 0, Pawn("black", (0, 4)), 0, Pawn("black", (0, 6)), 0],
        #               [0, Pawn("black", (1, 1)), 0, 1, 0, Pawn("black", (1, 5)), 0, Pawn("black", (1, 7))],
        #               [1, 0, Pawn("black", (2, 2)), 0, 1, 0, Pawn("black", (2, 6)), 0],
        #               [0, Pawn("black", (3, 1)), 0, Pawn("black", (3, 3)), 0, 1, 0, 1],
        #               [1, 0, 1, 0, 1, 0, 1, 0],
        #               [0, Pawn("white", (5, 1)), 0, Pawn("black", (5, 3)), 0, Pawn("black", (5, 5)), 0, Pawn("white", (5, 7))],
        #               [Pawn("white", (6, 0)), 0, Pawn("white", (6, 2)), 0, Pawn("white", (6, 4)), 0, Pawn("white", (6, 6)), 0],
        #               [0, Pawn("white", (7, 1)), 0, Pawn("white", (7, 3)), 0, Pawn("white", (7, 5)), 0, Pawn("white", (7, 7))]]

        self.draw_counter = 0

    def _print_board(self):
        """Prints board matrix as unicode GUI."""
        for i, row in enumerate(self.board):
            print(i + 1, end=" ")
            for j in row:
                print(u'◼', end=" ") if j == 0 else print(u'◻', end=" ") if j == 1 else print(j, end=" ")
            print("")
        print("  a b c d e f g h")
    
    def _convert_checker_coord(self, coord):
        """Given a coord (e.g: 'b4'), returns numerical coordinates (e.g: 4, 1)."""
        col = coord[:1]
        row = coord[1:]
        col = ord(col) - 96
        row = int(row)
        return (row - 1, col - 1)

    def _calculate_moves(self, position, already_coords=False):
        """Given the user's selected position, returns possible moves as a list."""
        row, col = self._convert_checker_coord(position) if already_coords == False else position
        piece = self.board[row][col]
        moves = piece.calculate_jump_moves(self.board)                     # If there are jump moves, we must do them!
        if not moves:
            return piece.calculate_simple_moves(self.board)      # if no jump moves, then return simple moves
        return moves

    def _execute_move(self, move):
        """Given the user's selected move, executes it and updates piece position."""
        b = move.beginning
        e = move.end
        self.board[e[0]][e[1]] = self.board[b[0]][b[1]]     # new territory, conquered!!
        self.board[b[0]][b[1]] = 1                          # deserted land left in the wake of battle
        self.board[e[0]][e[1]].location = e                 # update the piece instance's location attribute

        if isinstance(move, moves.Jump):
            for piece in move.eliminated:                   # removed jumped pieces
                row, col = piece.location
                self.board[row][col] = 1
            self.draw_counter = 0
        else:
            self.draw_counter += 1

        self._check_king(self.board[e[0]][e[1]])

    def _check_king(self, piece):
        """If a pawn has reached the end of the board, promote it to king."""
        c = piece.location
        if (c[0] == 0 and piece.color == "white") or (c[0] == 7 and piece.color == "black"):
            self.board[c[0]][c[1]] = King(piece.color, c)