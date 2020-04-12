"""Engine Settings

Include search Mode, initial position, and
piece string representation type.
"""

DEBUG = True

# Data files created during pregame setup.
DATA_DIRECTORY = 'data'

DATA_FILES = (
    BOARD_DATA_FILE, MOVE_DATA_FILE,
    MASK_DATA_FILE, EVALUATION_DATA_FILE
) = (
    'board.json', 'moves.json',
    'masks.json', 'evaluate.json'
)

# This determines engine search depth. If
# search mode is 'time,' the engine stops
# searching for a move after a static amount
# of time. If search mode is 'plies,' the
# engine stops searching based on a set amount
# of moves deep relative to current position.
SEARCH_TYPES = ['time','plies','ponder']
SEARCH_MODE = 'plies'

# used for pregame setup to create initial piece
# bitboards in pregame/generate/board.py. To
# try a new position, change this board str
# array and delete board.json. Rerunning the
# engine will then regenerate data/board.json
INITIAL_POSITION = [
    'R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R',
    'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
    'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
    'r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'
]

# determines the strings used to print pieces
# when chess.board.State.__str__ is called
PIECE_PRINT_MODE = 'UNICODE'
PIECE_REPRESENTATION = {
    'UNICODE': (
        ['♟', '♞', '♝','♜', '♛', '♚'],
        ['♙', '♘', '♗', '♖', '♕', '♔']
    ),
    'CHARS': (
        ['P', 'N', 'B', 'R', 'Q', 'K'],
        ['p', 'n', 'b', 'r', 'q', 'k']
    )
}[PIECE_PRINT_MODE]
