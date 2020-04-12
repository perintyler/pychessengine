# pychessengine


This engine contains 2 modules: pregame and chess. The pregame
modules precomputes moves for each piece, some board data, a few masks
and some evaluation stuff.

The chess module is where it all happens.
An engine can be categorized into
4 parts:
  - board representation (chess/board.py)
  - positional evaluation (chess/evaluation.py)
  - move generation (chess/move.py)
  - search (chess/search.py)
