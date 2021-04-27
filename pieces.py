import enum
from moves import Move, Simple, Jump

BLACK = 0
WHITE = 1

class Piece:
    def __init__(self, color):
        pass

class Pawn(Piece):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        if self.color == BLACK:
            return u'⚈'
        elif self.color == WHITE:
            return u'⚆'

    def _calculate_simple_moves(self, board, piece, row, col):
        if piece.color == BLACK:
            possible_moves = []
            for move in [Simple(board, (row, col), (row + 1, col - 1)), Simple(board, (row, col), (row + 1, col + 1))]:
                if move.end != None:
                    possible_moves.append(move)
            return possible_moves
        if piece.color == WHITE:
            return [(row - 1, col - 1), (row - 1, col + 1)]

    def _calculate_jump_moves(self, board, piece, row, col):
        pass

class King(Piece):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        if self.color == BLACK:
            return u'⚉'
        elif self.color == WHITE:
            return u'⚇'