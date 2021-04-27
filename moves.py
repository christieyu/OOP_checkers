class Move:
    def __init__(self, board, beginning, end):
        if end[0] < 0 or end[0] > 7 or end[1] < 0 or end[1] > 7 or board[end[0]][end[1]] != 1:
            self.end = None
        else:
            self.beginning = self._convert_matrix_coord(beginning)
            self.end = self._convert_matrix_coord(end)

    def _convert_matrix_coord(self, coord):
        """Given numerical coordinates (e.g: 4, 1), return coord (e.g: 'b4')."""
        row, col = coord
        return chr(col + 96 + 1) + str(row + 1)

class Simple(Move):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "simple"

class Jump(Move):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = "jump"
        self.history = [position]
