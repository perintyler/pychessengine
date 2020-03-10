# move_generation.py
# --------------------------------------------------------------
# This file is responsible for generating moves for every piece.
# Moves are generated as bitboards (see Bitboards.py), in which an
# on bit indicates that a square is a valid move destination.
# There are 2 types of move generation techniques used. For knights
# pawns, and kings, moves are precomputed and hashed. This is done
# by creating a move bitboard for each piece at every possible square.
# Since bitboards are just binary representations of integers, the hash
# is small and managable. The hashed bitboads store pseudo legal
# moves. Getting legal moves requires an extra step of bitwise
# operations to take into account occupied squares.
# The second type of piece generation is sliding piece generaton.
# The sliding pieces are rooks, bishops, and queens. Sliding piece
# moves are generated using file, rank, and diagonal masks (precomputed)
# as well as bitwise operations to account for 'blockers.' The algorithm
# is o^(o-2s), where o is the bitboard representing occupied squares,
# and s is the bitboard that stores the location of the 'slider.' This
# algorithm only generates moves in one direction, but getting moves in
# every direction can be achieved through Bitboard reversal.
# --------------------------------------------------------------
# https://www.chessprogramming.org/Move_Generation
# https://www.chessprogramming.org/Efficient_Generation_of_Sliding_Piece_Attacks
# https://www.chessprogramming.org/Subtracting_a_Rook_from_a_Blocking_Piece
# --------------------------------------------------------------

import masks
from color import Color
from bitboard import Bitboard
import json

class Move:
    def __init__(self, piece, endSquare, isACapture):
        self.piece = piece
        self.startSquare = piece.square
        self.endSquare = endSquare
        self.isACapture = isACapture

# temporary
class CastleMove(Move):
    def __init__(self):
        self.startSquare = -1
        self.piece = None
        self.endSquare = None 
        self.isACapture = False

# Returns all legal moves for every piece
def find_moves(board):
    pieces = board.get_player(board.colorToMove).pieces
    moves = []
    for piece in pieces:
        captureBB, nonCaptureBB = piece.get_moves(board)
        for endSquare in captureBB.get_on_bits():
            moves.append(Move(piece, endSquare, True))
        for endSquare in nonCaptureBB.get_on_bits():
            moves.append(Move(piece, endSquare, False))
    return moves


#################################################################
# PAWN/KNIGHT/KING                                              #        
#################################################################

# retrieve precomputed hashed move bitboards
with open('data/move_bitboards.json', 'r') as f:
    moveBitboards = json.load(f)

def get_hashed_moves(pieceChar, square, color=None):
    assert pieceChar == 'n' or pieceChar == 'p' or pieceChar == 'k'
    if pieceChar == 'n' or pieceChar == 'k':
        hashedMoveInt = moveBitboards[pieceChar][square]
        return Bitboard(hashedMoveInt)
    elif pieceChar == 'p':
        assert color is not None
        colorIndex = 0 if color == Color.WHITE else 1
        captureMoves = moveBitboards['p'][square][colorIndex][0]
        nonCaptureMoves = moveBitboards['p'][square][colorIndex][1]
        return Bitboard(captureMoves), Bitboard(nonCaptureMoves)

#################################################################
# SLIDING PIECES: BISHOP/ROOK/QUEEN                             #        
#################################################################

def get_straight_moves(index, occupied):
    # get file and rank masks to pass into generate_sliding_moves helper
    rankMask, fileMask = masks.get_rank_mask(index), masks.get_file_mask(index)
    horizontalMoves = generate_sliding_moves(index, occupied, rankMask)
    verticalMoves = generate_sliding_moves(index, occupied, fileMask)
    straightMoves = horizontalMoves | verticalMoves
    return straightMoves

def get_diagonal_moves(index, occupied):
    # get diagonal masks to pass into generate_sliding_moves helper
    diagonalMask = masks.get_diagonal_mask(index)
    antiDiagonalMask = masks.get_antidiagonal_mask(index)
    diagonalMoves = generate_sliding_moves(index, occupied, diagonalMask)
    antiDiagonalMoves = generate_sliding_moves(index, occupied, antiDiagonalMask)
    allDiagonals = diagonalMoves | antiDiagonalMoves
    return allDiagonals

# sliding piece move generation by calculation: o^(o-2s)
def generate_sliding_moves(index, occupied, mask):
    # create bitboard with single on bit at the sliders location
    slider = Bitboard(0)
    slider.turn_on_bit(index)

    # calculate positive rays
    potentialBlockers = occupied & mask
    positiveRay = occupied ^ (potentialBlockers - (slider*2))
    positiveRay = positiveRay & mask

    # reverse the Bitboards, then get negative rays
    occupiedReversed = reversed(occupied)
    maskReversed = reversed(mask)
    sliderReversed = reversed(slider)

    potentialBlockers = occupiedReversed & maskReversed
    negativeRay = occupiedReversed ^ (potentialBlockers - (sliderReversed*2))
    negativeRay = reversed(negativeRay & maskReversed)

    # combine positive and negative rays into one Bitboard and return
    return positiveRay | negativeRay