# from chess.board import PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING
# from chess.board import WHITE,BLACK
# from chess.board import INITIAL_STATE as STARTING_POSITION
# from chess.search import get_best_move
# from chess import board, search

# note: use boolean not to get opposite color
WHITE = 0
BLACK = 1

PIECE_TYPES = [PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING] = range(6)

GAME_STAGES = [OPENING, MIDGAME, ENDGAME] = range(3)

__all__ = ['board','move','search']

from chess.evaluate import Evaluator as PositionEvaluator

# def get_square(x,y):
#     return 8*y + x
#
# def get_coordinate(square):
#     x = square%8
#     y = int((square-x)/8)
#     return x,y



# def play():
#     import time
#     state = board.State.INITIAL
#
#     while True:
#         print(state)
#         start = time.time()
#         state = search.for_best_move(state)
#         end = time.time()
#         print('found move in ' + str(end - start) + ' seconds')


#################################################################
# PIECES			                 	                       	#
#################################################################
