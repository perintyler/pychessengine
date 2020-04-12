# -*- coding: utf-8 -*-
"""Pregame generation for values used by positional evaluation
    - Piece Square Table Value Lookups
    - Center Square Masks

TODO:
    - king/pawn strong masks
https://github.com/official-stockfish/Stockfish/blob/master/src/psqt.cpp
"""

import os
import json

from chess.bitboard import create as create_bitboard
from pregame.utils import get_coordinate,get_square


PIECE_SQUARE_TABLES = [
	# PAWN
	[0,  0,  0,  0,  0,  0,  0,  0,
	 50, 50, 50, 30, 30, 50, 50, 50,
	 5,  30, 5,  30, 30, 5,  30, 5,
	 3,  3, 10, 30, 30, 10,  3,  3,
	 0,  0,  0, 20, 20,  0,  0,  0,
	 5, -5,-10,  0,  0,-10, -5,  5,
	 5, 10, 10,-20,-20, 10, 10,  5,
	 0,  0,  0,  0,  0,  0,  0,  0],
	# KNIGHT
	[-50,-40,-30,-30,-30,-30,-40,-50,
	-40,-20,  0,  5,  5,  0,-20,-40,
	-30,  20, 10, 15, 15, 20, 0,-30,
	-30,  5, 15, 20, 20, 15,  5,-30,
	-30,  0, 15, 20, 20, 15,  0,-30,
	-30,  5, 10, 15, 15, 10,  5,-30,
	-40,-20,  0,  5,  5,  0,-20,-40,
	-50,-40,-30,-30,-30,-30,-40,-50,],
	# BISHOP
	[-20,-10,-10,-10,-10,-10,-10,-20,
	-10,  0,  0,  0,  0,  0,  0,-10,
	-10,  0,  5, 10, 10,  5,  0,-10,
	-10,  5,  5, 10, 10,  5,  5,-10,
	-10,  0, 10, 10, 10, 10,  0,-10,
	-10, 10, 10, 10, 10, 10, 10,-10,
	-10,  5,  0,  0,  0,  0,  5,-10,
	-20,-10,-10,-10,-10,-10,-10,-20,],
	# ROOK
	[0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,],
	# QUEEN
	[-20,-10,-10,  0, -5,-10,-10,-20,
	-10,  0,  0,  0,  0,  0,  0,-10,
	-10,  0,  5,  5,  5,  5,  0,-10,
	-5,  0,  5,  5,  5,  5,  0, -5,
	0,  0,  5,  5,  5,  5,  0, -5,
	-10,  5,  5,  5,  5,  5,  0,-10,
	-10,  0,  5,  0,  0,  0,  0,-10,
	-20,-10,-10, -5, -5,-10,-10,-20],
	# KING
	[0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,],
]

def generate_evaluation_data():

    def create_piece_square_table_lookup():
        """PST"""
        whiteLookups,blackLookups = [],[]
        for table in PIECE_SQUARE_TABLES:

            whiteLookupForPiece,blackLookupForPiece = {},{}
            for square in range(64):
                squareBitboard = create_bitboard([square])
                whiteLookupForPiece[squareBitboard] = table[square]

                # tables are upside down for black. Flip the y value
                x,y = get_coordinate(square)
                flippedSquare = get_square(x,7-y)
                blackLookupForPiece[squareBitboard] = table[flippedSquare]

            whiteLookups.append(whiteLookupForPiece)
            blackLookups.append(blackLookupForPiece)

        return [whiteLookups,blackLookups]

    return {'PST': create_piece_square_table_lookup()}

    # def create_center_square_masks():
    # 	"""Generates a mask for each center squares and outer center square"""
    # 	centerSquares = [E4, D4, E5, D5]
    # 	outerCenterSquares = [F3, F4, F5, F6, C3,C4, C5, C6, E3, D3, E6, D6]
    #
    #     centerSquareMasks = [Bitboard([sq]) for sq in centerSquares]
    #     outCenterSquareMasks = [Bitboard([sq]) for sq in outerCenterSquares]
    # 	return {'center':centerSquareMasks, 'outer-center':outCenterSquareMasks}
    # return {
    #     'squares': create_center_square_masks(),
    #     'PST': create_piece_square_table_lookup()
    # }
