PIECES = {
    0: u'◼',
    1: u'⚆',
    2: u'⚈',
    3: u'⚇',
    4: u'⚉',
    5: u'◻',
}

class Board:
    def __init__(self, p1="human", p2="human", history=False):
        self.board = [[2, 0, 2, 0, 2, 0, 2, 0],
                      [0, 2, 0, 2, 0, 2, 0, 2],
                      [2, 0, 2, 0, 2, 0, 2, 0],
                      [0, 5, 0, 5, 0, 5, 0, 5],
                      [5, 0, 5, 0, 5, 0, 5, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1]]

    def _print_board(self):
        """Print numerical matrix as board GUI."""
        for i, row in enumerate(self.board):
            print(i + 1, ' '.join(map(PIECES.get, row)))
        print("  a b c d e f g h")
    
    def _convert_checker_coord(coord):
        """Given a coord (e.g: 'b4'), return numerical coordinates (e.g: 4, 1)."""
        col = coord[:1]
        row = coord[1:]
        col = ord(col) - 96
        row = int(row)
        return (row - 1, col - 1)

    def _convert_matrix_coord(coord):
        """Given numerical coordinates (e.g: 4, 1), return coord (e.g: 'b4')."""
        row, col = coord
        return chr(col + 96 + 1) + str(row + 1)