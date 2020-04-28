# pychessengine

The engine can be categorized into 4 parts, each of which has its own
file in the chess module:
  - board representation (board.py)
  - positional evaluation (evaluate.py)
  - move generation (move.py)
  - game tree search (search.py)

## Board Representation

This engine uses a Piece List approach. A board state stores a list of pieces
and occupancy bitboards. Board state has to be maintained and updated to
traverse a decision tree. This requires being able to  efficiently update and
revert a board state. This is done through bitwise operations on the piece
and occupancy bitboards, as well as Zobrist Hashing (https://en.wikipedia.org/wiki/Zobrist_hashing)

### Bitboards

A bitboard is a 64 bit integer where each bit corresponds to a square on the
board. Bitboards are powerful because they can be manipulated using bitwise
operations to perform computations that would otherwise only be possible
through iterating through squares on the board.
Learn More: https://en.wikipedia.org/wiki/Bitboard

### Piece Sets

Each piece bitboard contains a single on bit indicating the square the piece is
on. There are 32 pieces at the start of a chess game, so a board state can be
stored and maintained with just 32 integers: 256 bytes. Piece bitboards are
never removed from a board state. Following a move (which is also represented
as a bitboard), piece bitboards are updated using bitwise operations. If the
move is a capture, the captured piece becomes an empty bitboard. This way,
scanning through individual bits in a bitboard can be avoided. Checking if a
bitboard is empty is efficient because it can be done with a simple equality
check, since an an empty bitboard will be equal to 0.

## Evaluation

A positive score indicates white is winning, while a negative
score means black is winning. A score is determined for each property,
which then is multiplied by a weight. Weights are currently hardcoded in, but
I plan to create some type of regression to optimize them.

Evaluation Function
	- Heuristic 		  	  -- https://en.wikipedia.org/wiki/Heuristic_(computer_science)
	- Linear Combinations -- https://en.wikipedia.org/wiki/Linear_combination

Evaluation Discontinuity
	- Discontinuity 	  	-- https://www.chessprogramming.org/Evaluation_Discontinuity
	- Tapered Evaluation  -- https://www.chessprogramming.org/Tapered_Eval
	- Game Phases			    -- https://www.chessprogramming.org/Game_Phases

Evaluation Features
	- Material            -- https://www.chessprogramming.org/Material
  - Piece Square Tables -- https://www.chessprogramming.org/Piece-Square_Tables
	- Center Control      -- https://www.chessprogramming.org/Center_Control
	- Mobility            -- https://www.chessprogramming.org/Mobility
	- Connectivity        -- https://www.chessprogramming.org/Connectivity
	- Development         -- https://www.chessprogramming.org/Development

## Search

Searching for the optimal move in a game tree. Moves are edges, board
states are nodes.

### Minimax with Alpha-Beta pruning

Finds optimal positions. The engine uses a minimax search with alpha-beta
pruning which has a time complexity of O(b^d), where b is the number of legal
moves and d is the maximum search depth. A minimax search minimizes loss by
finding the optimal worst possible outcome. It is a depth first search that
eliminates branches if a player's optimal worst position is worse than the
opponents optimal worst outcome. This is possible because chess is a zero sum
game.

Minimax: https://en.wikipedia.org/wiki/Minimax
Alpha-Beta: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

## Moves Generation

Moves are represented as bitboards. Move generation is done in 2 steps.
Attack generation and legal move generation. Moves are generation using
bitwise operations and precomputed/cached move bitboards generated in
the pregame module. Magic bitboards for sliding piece attacks.

Magic bitboards: https://www.chessprogramming.org/Magic_Bitboards

### Move Ordering

https://www.chessprogramming.org/Move_Ordering

## Pregame Module

The pregame modules precomputes a move cache, and generates board/evaluation
data.
