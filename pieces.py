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

class King(Piece):
    def __init__(self, color):
        self.color = color

    def __str__(self):
        if self.color == BLACK:
            return u'⚉'
        elif self.color == WHITE:
            return u'⚇'