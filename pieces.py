import enum
from moves import Move, Simple, Jump

BLACK = 0
WHITE = 1

class Piece:
    def __init__(self, color):
        """Initializes piece."""
        self.color = color

    def _calculate_jump_moves(self, board, piece, row, col):
        """Calculates jump moves diagonally forward & left/right for a pawn piece."""
        pass

class Pawn(Piece):
    def __str__(self):
        """Handles printing characters for pawns."""
        if self.color == BLACK:
            return u'⚈'
        elif self.color == WHITE:
            return u'⚆'

    def _calculate_simple_moves(self, board, piece, row, col):
        """Calculates simple moves diagonally forward & left/right for a pawn piece."""
        possible_moves = []
        if piece.color == BLACK:
            for move in [Simple(board, (row, col), (row + 1, col - 1)), 
                         Simple(board, (row, col), (row + 1, col + 1))]:
                if move.end != None:
                    possible_moves.append(move)
        else:
            for move in [Simple(board, (row, col), (row - 1, col - 1)), Simple(board, (row, col), (row - 1, col + 1))]:
                if move.end != None:
                    possible_moves.append(move)
        return possible_moves

class King(Piece):
    def __str__(self):
        """Handles printing characters for kings."""
        if self.color == BLACK:
            return u'⚉'
        elif self.color == WHITE:
            return u'⚇'

    def _calculate_simple_moves(self, board, piece, row, col):
        """Calculates simple moves diagonally forward/backward & left/right for a king piece."""
        possible_moves = []
        for move in [Simple(board, (row, col), (row + 1, col - 1)),
                     Simple(board, (row, col), (row + 1, col + 1)),
                     Simple(board, (row, col), (row - 1, col - 1)),
                     Simple(board, (row, col), (row - 1, col + 1))]:
            if move.end != None:
                possible_moves.append(move)
        return possible_moves