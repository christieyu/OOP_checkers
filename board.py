from pieces import Piece, Pawn, King, BLACK, WHITE

class Board:
    def __init__(self, p1="human", p2="human", history=False):
        """Initialize board where 0 is an unplayable space and 1 is a playable space."""
        self.board = [[Pawn(BLACK), 0, Pawn(BLACK), 0, Pawn(BLACK), 0, Pawn(BLACK), 0],
                      [0, Pawn(BLACK), 0, Pawn(BLACK), 0, Pawn(BLACK), 0, Pawn(BLACK)],
                      [Pawn(BLACK), 0, Pawn(BLACK), 0, Pawn(BLACK), 0, Pawn(BLACK), 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, Pawn(WHITE), 0, Pawn(WHITE), 0, Pawn(WHITE), 0, Pawn(WHITE)],
                      [Pawn(WHITE), 0, Pawn(WHITE), 0, Pawn(WHITE), 0, Pawn(WHITE), 0],
                      [0, Pawn(WHITE), 0, Pawn(WHITE), 0, Pawn(WHITE), 0, Pawn(WHITE)]]

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

    def _calculate_moves(self, position):
        """Given the user's selected position, returns possible moves as a list."""
        row, col = self._convert_checker_coord(position)
        piece = self.board[row][col]
        # If there are jump moves, we must do them
        if piece._calculate_jump_moves(self.board, piece, row, col) == None:
            return piece._calculate_simple_moves(self.board, piece, row, col)
        return piece._calculate_jump_moves(self.board, piece, row, col)

    def _execute_move(self, move):
        """Given the user's selected move, executes it."""
        if move.type == "simple":
            beginning = self._convert_checker_coord(move.beginning)
            end = self._convert_checker_coord(move.end)
            self.board[end[0]][end[1]] = self.board[beginning[0]][beginning[1]]
            self.board[beginning[0]][beginning[1]] = 1