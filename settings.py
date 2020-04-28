# -*- coding: utf-8 -*-
"""Engine Settings"""

DEBUG = True

# If true, the engine plays against itself.
# If False, the engine plays against a user
COMPUTER_PLAY = True

# How many moves ahead the engine searches
SEARCH_DEPTH = 5

# Data files created during pregame setup.
DATA_DIRECTORY = 'data'

# used for pregame setup to create initial piece
# bitboards in pregame/generate/board.py. To
# try a new position, change this board str
# array and delete board.json. Rerunning the
# engine will then regenerate data/board.json
INITIAL_POSITION = [
    'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
    'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
    'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R',
]

# for printing board.State
PIECE_PRINT_MODE = 'UNICODE'
PIECE_REPRESENTATION = {
    'UNICODE': (
        ['♙', '♘', '♗', '♖', '♕', '♔'],
        ['♟', '♞', '♝','♜', '♛', '♚']
    ),
    'CHARS': (
        ['P', 'N', 'B', 'R', 'Q', 'K'],
        ['p', 'n', 'b', 'r', 'q', 'k']
    )
}[PIECE_PRINT_MODE]
