from pregame.load import *
# from data.hash_key import RANDOM_ARRAY as ZOBRIST_HASH_TABLE

# save data for chess/move.py
MOVES,MOVE_SETS = load_move_data()
MOVE_MASKS = load_masks()

# save data for chess/evaluate.py
PST_LOOKUP = load_evaluation_data()

# save data for chess/board.py
(ZOBRIST_HASH_TABLE, INITIAL_PIECES,
 NUM_PIECES, PIECE_TYPE_LOOKUP,
 COLOR_LOOKUP, COLOR_RANGES) = load_board_data()
