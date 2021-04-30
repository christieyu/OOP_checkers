from pieces import Piece, Pawn, King, BLACK, WHITE
import moves

class Board:
    def __init__(self, p1="human", p2="human", history=False):
        """Initialize board where 0 is an unplayable space and 1 is a playable space."""

        # this is the standard starting layout! wowzers!
        # (ok yeah this looks terrible I'm sorry maybe we can change later? idk)
        # self.board = [[Pawn(BLACK, (0, 0)), 0, Pawn(BLACK, (0, 2)), 0, Pawn(BLACK, (0, 4)), 0, Pawn(BLACK, (0, 6)), 0],
        #               [0, Pawn(BLACK, (1, 1)), 0, Pawn(BLACK, (1, 3)), 0, Pawn(BLACK, (1, 5)), 0, Pawn(BLACK, (1, 7))],
        #               [Pawn(BLACK, (2, 0)), 0, Pawn(BLACK, (2, 2)), 0, Pawn(BLACK, (2, 4)), 0, Pawn(BLACK, (2, 6)), 0],
        #               [0, 1, 0, 1, 0, 1, 0, 1],
        #               [1, 0, 1, 0, 1, 0, 1, 0],
        #               [0, Pawn(WHITE, (5, 1)), 0, Pawn(WHITE, (5, 3)), 0, Pawn(WHITE, (5, 5)), 0, Pawn(WHITE, (5, 7))],
        #               [Pawn(WHITE, (6, 0)), 0, Pawn(WHITE, (6, 2)), 0, Pawn(WHITE, (6, 4)), 0, Pawn(WHITE, (6, 6)), 0],
        #               [0, Pawn(WHITE, (7, 1)), 0, Pawn(WHITE, (7, 3)), 0, Pawn(WHITE, (7, 5)), 0, Pawn(WHITE, (7, 7))]]

        # lookie here! it's a modified board for looking at jumps! wowzers!
        self.board = [[Pawn(BLACK, (0, 0)), 0, 1, 0, Pawn(BLACK, (0, 4)), 0, Pawn(BLACK, (0, 6)), 0],
                      [0, Pawn(BLACK, (1, 1)), 0, 1, 0, Pawn(BLACK, (1, 5)), 0, Pawn(BLACK, (1, 7))],
                      [1, 0, Pawn(BLACK, (2, 2)), 0, 1, 0, Pawn(BLACK, (2, 6)), 0],
                      [0, Pawn(BLACK, (3, 1)), 0, Pawn(BLACK, (3, 3)), 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, Pawn(WHITE, (5, 1)), 0, Pawn(BLACK, (5, 3)), 0, Pawn(BLACK, (5, 5)), 0, Pawn(WHITE, (5, 7))],
                      [Pawn(WHITE, (6, 0)), 0, Pawn(WHITE, (6, 2)), 0, Pawn(WHITE, (6, 4)), 0, Pawn(WHITE, (6, 6)), 0],
                      [0, Pawn(WHITE, (7, 1)), 0, Pawn(WHITE, (7, 3)), 0, Pawn(WHITE, (7, 5)), 0, Pawn(WHITE, (7, 7))]]


    def _print_board(self):
        """Prints board matrix as unicode GUI."""
        for i, row in enumerate(self.board):
            print(i + 1, end=" ")
            for j in row:
                if j == 0:
                    print(u'◼', end=" ")
                elif j == 1:
                    print(u'◻', end=" ")
                else:
                    print(j, end=" ")
            print("")
        print("  a b c d e f g h")
    
    def _convert_checker_coord(self, coord):
        """Given a coord (e.g: 'b4'), returns numerical coordinates (e.g: 4, 1)."""
        col = coord[:1]
        row = coord[1:]
        col = ord(col) - 96
        row = int(row)
        return (row - 1, col - 1)

    def _check_selection(self, piece):
        """Checks if a selected space is legal for this move (e.g. piece has correct 
        color for this turn, the board position contains a piece, etc)"""
        # check if piece can move
        # check if piece exists at location
        # check if player owns this piece
        pass

    def _calculate_moves(self, position):
        """Given the user's selected position, returns possible moves as a list."""
        row, col = self._convert_checker_coord(position)
        piece = self.board[row][col]
        self._check_selection(piece)
        moves = piece._calculate_jump_moves(self.board)                     # If there are jump moves, we must do them!
        if not moves:
            return piece._calculate_simple_moves(self.board, row, col)      # if no jump moves, then return simple moves
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


            