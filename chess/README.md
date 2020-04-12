# pychessengine

## Todo
  - make move bitboards a dict take takes bitboard, not square
  - get evaluation properties working again
  - remove position logic from search logic
  - finalize zobrist hashing
  - Quiescence search
  - board distances
  - neural net for evaluation weights
  - neural net for pst values
  - magic bitboards (https://www.chessprogramming.org/Magic_Bitboards)
  - Principle Variation Search

## About

categorized into 4 categories
  - Board Representation: board.py
  - Move generation: move.py
  - Evaluation: evalute.py
  - Search: search.py

Zobrist Hashing, Minimax, Alpha beta pruning, Bitboards

## Board Representation

A board is represented as a list of piece bitboards.

### Bitboards

A bitboard is a 64 bit integer where each bit corresponds to a square on the
board. Bitboards are powerful because they can be manipulated using bitwise
operations to perform computations that would otherwise only be possible
through iterating through squares on the board.

### Piece Sets

Each piece bitboard contains a single on bit indicating the square the piece is
on. There are 32 pieces at the start of a chess game,
so a board state can be stored and maintained with just 32 integers: 256 bytes.
Piece bitboards are never removed from a board state. Following a move (which
is also represented as a bitboard), piece bitboards are updated using bitwise
operations. If the move is a capture, the captured piece becomes an empty
bitboard. This way, scanning through individual bits in a bitboard can be avoided.
Checking if a bitboard is empty is efficient because it can be done with a simple
equality check. Since a bitboard is just an integer, an empty bitboard will be
equal to 0.

## Evaluation

A positive evaluation means that white has an advantage, and a negative
evaluation reflects that black has an advantage.

Evaluation properties used:
  - Material
  - Connectivity
  - Mobility
  - Center Control
  - Pawn Structure
    - # of Doubled Pawns
    - # of Isolated Pawns
    - # of Center Pawns
  - Piece Square Tables
  - Development
  - Bishop Pair Bonus


A score is determined for each property, which then is multiplied by a
weight. Weights are currently hardcoded in, but I plan to train some type
of net to determine optimal weights for each property.


## Move Generation and Validation

Moves are
represented as bitboards. Move generation consists of
two steps: pseudo legal move generation and legal move generation. Pseudo
legal moves do not consider if the king is in check. They are also used
to compute attack bitboards, which is used for positional evaluation. For
the most part, pseudo legal moves for each piece for each square are
precomputed and stored in memory. Precomputed Pseudo legal moves can then
be used to compute legal moves with bitwise operations. For sliding piece
move generation (Bishops, Rooks, and Queens), legal moves are computed
using bitwise "blocker" subtraction using an algorithm called o^(o-2s).



## Search

## Alpha-Beta

finds optimal
positions. It uses a minimax search with alpha-beta pruning
which has a time complexity of O(b^d), where b is the number
of legal moves and d is the maximum search depth. A minimax
search minimizes loss by finding the optimal worst possible
outcome. It is a depth first search that eliminates branches
if a player's optimal worst position is worse than the openents
optimal worst ouotcome. This is possible because chess is a
zero sum game.

 - https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
 - https://en.wikipedia.org/wiki/Minimax

  - https://en.wikipedia.org/wiki/MTD-f
  - https://en.wikipedia.org/wiki/Best_node_search
