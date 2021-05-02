# Christie Yu, Matt Udry
# CPSC 327 (Object Oriented Programming) Homework 4

class PlayerState:
    def __init__(self, CLI):
        self.CLI = CLI
        self.moves = []
        self.pieces_left = True

    def _toggle_color(self):
        pass

class WhiteState(PlayerState):
    def __init__(self, CLI, p1):
        super().__init__(CLI)
        self.color = "white"
        self.player = p1

    def __str__(self):
        return "white"

    def _toggle_color(self):
        self.CLI.player_state = self.CLI.black_state

class BlackState(PlayerState):
    def __init__(self, CLI, p2):
        super().__init__(CLI)
        self.color = "black"
        self.player = p2

    def __str__(self):
        return "black"

    def _toggle_color(self):
        self.CLI.player_state = self.CLI.white_state
        

class PlayerMove:

    def __init__(self, turn_num, player_state, move_obj, board_state):
        self.turn_num = turn_num
        self.player_state = player_state
        self.move_obj = move_obj
        self.board_state = board_state

    def execute(self, current_board):
        current_board._execute_move(self.move_obj)