class Move:
    def __init__(self, board, beginning, end):
        """Initializes move and checks that its ending location is within bounds."""
        if end[0] < 0 or end[0] > 7 or end[1] < 0 or end[1] > 7 or board[end[0]][end[1]] != 1:
            self.end = None
        else:
            self.beginning = self._convert_matrix_coord(beginning)
            self.end = self._convert_matrix_coord(end)

    def _convert_matrix_coord(self, coord):
        """Given numerical coordinates (e.g: 4, 1), returns coord (e.g: 'b4')."""
        row, col = coord
        return chr(col + 96 + 1) + str(row + 1)

class Simple(Move):
    def __init__(self, *args, **kwargs):
        """Initializes simple move."""
        super().__init__(*args, **kwargs)
        self.type = "simple"

class Jump(Move):
    def __init__(self, *args, **kwargs):
        """Initializes jump move and creates location archive."""
        super().__init__(*args, **kwargs)
        self.type = "jump"
        self.history = [position]