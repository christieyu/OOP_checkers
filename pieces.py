# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

import enum
from moves import Move, Simple, Jump

WHITE_MOVES = [(-1, 1), (-1, -1)]
BLACK_MOVES = [(1, 1), (1, -1)]

class Piece:
    def __init__(self, color, location):
        self.color = color
        self.location = location
        self.moves = WHITE_MOVES if color == "white" else BLACK_MOVES

    def calculate_simple_moves(self, board):
        """Calculates simple moves for a piece."""
        possible_moves = []
        for direction in self.moves:
            if self._get_adjacent(board, self.location, direction) == 1:
                adj_coord = self._get_adjacent(board, self.location, direction, True)
                possible_moves.append(Simple(self.location, adj_coord))
        return possible_moves

    def _has_jumpback(self, branch: Jump, prev_move: Jump):
        """Template method for checking if a possible jump branch loops back onto itself."""
        pass

    def calculate_jump_moves(self, board):
        """Given the board, calculates jump moves for this piece. Returns a list of the possible jumping paths."""
        possible_moves = []
        for direction in self.moves:
            jump = self._check_jump(board, self.location, direction)
            if jump != None:
                ghost = Pawn(self.color, jump.end)                                                  # see if more jumps exist on this path
                branches = ghost.calculate_jump_moves(board)                                        # recurse from the position we jumped to!
                if branches:
                    for move in branches:
                        if self._has_jumpback(move, jump):
                            continue
                        jump_branch = Jump(self.location, move.end, move.eliminated)                # not quite sure how this works, sry :(
                        jump_branch.eliminated = jump.eliminated + jump_branch.eliminated           # append eliminated pieces from later on in branch
                        possible_moves.append(jump_branch)
                else:
                    possible_moves.append(jump)                                                     # if no branches, return this jump as destination
        return possible_moves

    def _get_adjacent(self, board, start: tuple, direction: tuple, return_coord=False):
        """Fetches obj or value at location in a given starting point and direction (if it exists)"""
        return self._get_board(board, (start[0] + direction[0], start[1] + direction[1]), return_coord)

    def _get_board(self, board, coords, return_coord=False):
        """Fetches obj or value at a given board location (if it exists)"""
        if coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7:
            return None
        if return_coord:
            return (coords[0], coords[1])               # return the coordinates at board location
        return board[coords[0]][coords[1]]              # return the value at board location    


    def _check_jump(self, board, start: tuple, direction: tuple):
        """Given a starting location and direction (both coordinate tuples), returns a Jump object (for a single jump)
        If no jumps are possible, returns None."""
        adj = self._get_adjacent(board, start, direction)
        if isinstance(adj, Piece):
            if adj.color != self.color and self._get_adjacent(board, adj.location, direction) == 1:
                end = self._get_adjacent(board, adj.location, direction, True)
                return Jump(start, end, adj)
        return None


class Pawn(Piece):
    def __str__(self):
        return u'???' if self.color == "black" else u'???'

    def _has_jumpback(self, branch, prev_move):
        False                                               # can't jump backwards, no need to check


class King(Piece):
    def __init__(self, color, location):
        self.color = color
        self.location = location       
        self.moves = WHITE_MOVES + BLACK_MOVES

    def __str__(self):
        return u'???' if self.color == "black" else u'???'

    def _has_jumpback(self, branch, prev_move):
        """Template method for checking if a possible jump branch loops back onto itself."""
        if branch.end == prev_move.beginning:
            return True
        return False