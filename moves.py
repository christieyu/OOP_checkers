# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

class Move:
    def __init__(self, beginning, end):
        """Initializes move and checks that its ending location is within bounds."""
        if end[0] < 0 or end[0] > 7 or end[1] < 0 or end[1] > 7:
            self.end = None
        else:
            self.beginning = beginning
            self.end = end

    def _convert_matrix_coord(self, coord):
        """Given numerical coordinates (e.g: 4, 1), returns coord (e.g: 'b4')."""
        row, col = coord
        return chr(col + 96 + 1) + str(row + 1)

class Simple(Move):
    def __init__(self, *args, **kwargs):
        """Initializes simple move."""
        super().__init__(*args, **kwargs)
        self.type = "simple"
        self.eliminated = []

    def __str__(self):
        beginning = self._convert_matrix_coord(self.beginning)
        end = self._convert_matrix_coord(self.end)
        return f"basic move: {beginning}->{end}"

class Jump(Move):
    def __init__(self, beginning, end, elim):
        """Initializes jump move and creates location archive."""
        super().__init__(beginning, end)
        self.type = "jump"
        self.eliminated = [elim]        # contains list of eliminated enemy piece objects
        if isinstance(elim, list):
            self.eliminated = elim      # overwrite in case elim was passed in as a list

    def __str__(self):
        beginning = self._convert_matrix_coord(self.beginning)
        end = self._convert_matrix_coord(self.end)
        captured = ", ".join([self._convert_matrix_coord(piece.location) for piece in self.eliminated])
        return f"jump move: {beginning}->{end}, capturing [{captured}]"
