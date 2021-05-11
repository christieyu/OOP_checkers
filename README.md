# Object-Oriented Checkers Implementation in Python
Implementation of checkers for CPSC 327 (Object Oriented Programming) at Yale by Christie Yu and Matt Udry.

## Project Description

In this project, we implemented checkers in Python using object-oriented strategies. We used [usual English draught rules](https://en.wikipedia.org/wiki/English_draughts) except jumping is mandatory: if the player or bot can jump, they must. The board is represented thus:

    1 ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼
    2 ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈
    3 ⚈ ◼ ⚈ ◼ ⚈ ◼ ⚈ ◼
    4 ◼ ◻ ◼ ◻ ◼ ◻ ◼ ◻
    5 ◻ ◼ ◻ ◼ ◻ ◼ ◻ ◼
    6 ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆
    7 ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼
    8 ◼ ⚆ ◼ ⚆ ◼ ⚆ ◼ ⚆
      a b c d e f g h
      
Where a '⚆' represents a pawn piece and a '⚇'represents a king piece.

Once a user selects a piece to move by calling its coordinate (e.g: 'c3'), the program returns a list of moves that the user must choose from.

There are three kinds of players in the game: human (player submits moves), random (computer chooses a random move from the moveset, prioritizing jumps), and greedy (computer chooses the move from the moveset with the most jumps, breaking ties randomly).

The program also has move undo/redo functionality.

## Running the program

To run the program, write to the command line:

`python3 main.py [arg1] [arg2] [arg3]`

* `arg1` should be `human`, `random` or `greedy`; is `human` by default; and represents the type of player that plays white.
* `arg2` should be `human`, `random` or `greedy`; is `human` by default; and represents the type of player that plays black.
* `arg3` should be `on` or `off`; is `off` by default; and represents whether the game offers undo/redo functionality.

For example, the input `python3 main.py` represents a game played by two humans without undo/redo functionality.

Meanwhile, the input `python3 main.py random greedy on` represents a game played by a random bot on white, a greedy bot on black, and undo/redo functionality.


## Methods

For this assignment, we created classes for the CLI, board, players, pieces, and moves, all of which should be transferable to a future implementation of chess or any other board, turn-based game. Specific design patterns we chose to implement include the **state, strategy, command, and template pattern**.

We first chose the **state pattern** to switch between player colors each turn so that we could retrieve players’ attributes (their possible moves, whether or not they have pieces left, their print strings) without using “if white” or “if black” statements. Designing the players’ colors as objects also allows for flexibility in attributes tied to each color or total numbers of colors for other board, turn-based games. Chess, for instance, would also utilize “white player” and “black player” states, but might have different info attached to each (whether each has a queen, for instance), which we can easily add to our states. Chinese checkers, as another example, has similar rules to English draughts but uses a star-of-David shaped board that includes three players. To implement that, we can just add another color to our state machine.

We then implemented a **strategy pattern** to select actions from “human,” “random,” and “greedy” player types. This was similar to our first homework assignment when we selected bank actions from a menu. This kind of menu structure eliminates the need for lengthy if-else statements and leaves room for the implementation of new player types. Even though our current implementation only has three options, perhaps an extended implementation might have a “novice random” player and an “advanced random” player with different levels of intelligence. Since these player types are essentially interchangeable in the code — the only difference being the specific move they select — the strategy pattern works well for this case.

For the pieces (namely the pawns and kings), we used a **template method** to reduce duplication in the jump calculations. Since the steps for pawns and kings to jump are nearly identical except for one key difference — the directions they are allowed to jump in — we extracted that single step into a method in each piece’s subclass, which then returns to the parent method with each piece’s possible directions. Because board-based games have many types of pieces and rules of how they can move (chess, as one example), such a template method will easily account for rules of jumping for any added pieces.

Finally, we used a **command pattern** to keep track of the entire board’s state after each move. The “player move” object collects variables such as the turn number, player state, move state, and board state to store these as parameters for other functions. By doing so, we can easily implement “undo” and “redo” options. In an expanded implementation of a board, turn-based game, we can also use the history of the “player move” object (which we called “move history”) to reconstruct the entire game if the user wishes. This would be useful for summarizing or reviewing game footage.

## UML Diagram
![Checkers UML diagram](https://user-images.githubusercontent.com/43098796/117768323-3989ac00-b200-11eb-9097-19788a522fd0.png)
