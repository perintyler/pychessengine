# pst.py
# --------------------------------------------------------------- 
# This file contains piece square tables, which is used to evaluate
# positions. A piece square table assigns a value to every square
# for each piece, indicating how strong a given piece is on a given
# square. To get a piece's square value, use the get_pst_value 
# function at the bottom of this file.
# --------------------------------------------------------------- 

from color import BLACK

MIN_VALUE = -20
MAX_VALUE = 20

PIECE_SQUARE_TABLES = {
    'P': [0,  0,  0,  0,  0,  0,  0,  0,
          50, 50, 50, 30, 30, 50, 50, 50,
          10, 30, 5,  30, 30, 5,  30, 10,
          3,  3, 10, 30, 30, 10,  3,  3,
          0,  0,  0, 20, 20,  0,  0,  0,
          5, -5,-10,  0,  0,-10, -5,  5,
          5, 10, 10,-20,-20, 10, 10,  5,
          0,  0,  0,  0,  0,  0,  0,  0
    ],
    'N': [-50,-40,-30,-30,-30,-30,-40,-50,
          -40,-20,  0,  5,  5,  0,-20,-40,
          -30,  20, 10, 15, 15, 20, 0,-30,
          -30,  5, 15, 20, 20, 15,  5,-30,
          -30,  0, 15, 20, 20, 15,  0,-30,
          -30,  5, 10, 15, 15, 10,  5,-30,
          -40,-20,  0,  5,  5,  0,-20,-40,
          -50,-40,-30,-30,-30,-30,-40,-50,],
    'B': [-20,-10,-10,-10,-10,-10,-10,-20,
          -10,  0,  0,  0,  0,  0,  0,-10,
          -10,  0,  5, 10, 10,  5,  0,-10,
          -10,  5,  5, 10, 10,  5,  5,-10,
          -10,  0, 10, 10, 10, 10,  0,-10,
          -10, 10, 10, 10, 10, 10, 10,-10,
          -10,  5,  0,  0,  0,  0,  5,-10,
          -20,-10,-10,-10,-10,-10,-10,-20,],
    'R': [0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,],
    'Q': [-20,-10,-10,  0, -5,-10,-10,-20,
          -10,  0,  0,  0,  0,  0,  0,-10,
          -10,  0,  5,  5,  5,  5,  0,-10,
           -5,  0,  5,  5,  5,  5,  0, -5,
            0,  0,  5,  5,  5,  5,  0, -5,
          -10,  5,  5,  5,  5,  5,  0,-10,
          -10,  0,  5,  0,  0,  0,  0,-10,
          -20,-10,-10, -5, -5,-10,-10,-20],
    'K': [0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,],
}


def get_square_value(piece):
    pieceChar = piece.as_char().upper()
    square = piece.square
    # tables are flipped for black
    if piece.color == BLACK:
        x = square % 8
        y = square // 8
        y = 7-y
        square = y*8 + x
    return PIECE_SQUARE_TABLES[pieceChar][square]