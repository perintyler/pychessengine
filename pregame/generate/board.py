"""Pregame setup for board module

Board data is generated and saved to 'data/board.json'. This includes:
    - initial position data
        + piece bitboards
        + piece indexing (see PieceSet in board.py for how pieces are indexed)
    - zobrist hash key
        + https://en.wikipedia.org/wiki/Zobrist_hashing
"""
import os
import json

from chess.bitboard import create as create_bitboard
from chess import WHITE, BLACK
from chess import PIECE_TYPES
from settings import INITIAL_POSITION


"""Generates Zobrist Hash Key"""
def generate_hash_key():
    """Random bitstrings for  each piece element"""
    return []

def generate_board_data():

    # For invalid chars in board str array
    class InvalidInitialPositionException(Exception): pass

    def parse_board_str():
        allChars = ('p','n','b','r','q','k')
        charPieceTypeDict = {c:pt for c,pt in zip(allChars,PIECE_TYPES)}

        # create initially empty piece type dicts for white/black
        pieces = {
            WHITE: {pieceType:[] for pieceType in PIECE_TYPES},
            BLACK: {pieceType:[] for pieceType in PIECE_TYPES}
        }

        # iterate over board str array and if str at square is not empty, add
        # piece type and square to initial piece dict. white piece are uppercase
        for square, char in enumerate(INITIAL_POSITION):
            if char == ' ': continue
            color = WHITE if char.isupper() else BLACK
            char = char.lower()

            if char not in charPieceTypeDict:
                errorMsg = f"invalid char '{char}' at square index {square}"
                raise InvalidInitialPositionException(errorMsg)
            else:
                pieceType = charPieceTypeDict[char]
                pieces[color][pieceType].append(square)

        return pieces

    def setup_piece_indexing(pieceTypes):
        # (colorRanges,
        #  typeRanges,
        #  pieceTypeLookup,
        #  colorLookup) = [],[],[],[] # indexers

        colorRanges, colorLookup,pieceTypeLookup = [],[],[]

        pieceIndex = 0
        for color in (WHITE,BLACK):
            # add color range for all piece types
            numPiecesForColor = sum(map(len, pieceTypes[color].values()))
            rangeForColor = (pieceIndex, pieceIndex+numPiecesForColor)
            colorRanges.append(rangeForColor)

            # create range for each individual piece type of color
            # typeRangesForColor = {}
            for pieceType,squareForType in pieceTypes[color].items():
                # numPiecesOfType = len(squareForType)
                # pieceTypeRange = (pieceIndex,pieceIndex+numPiecesOfType)
                # typeRangesForColor[pieceType] = pieceTypeRange

                # update lookups by adding the type/color for each piece of type
                numPiecesOfType = len(squareForType)
                pieceTypeLookup += numPiecesOfType*[pieceType]
                colorLookup     += numPiecesOfType*[color]
                pieceIndex += numPiecesOfType

            # add piece type ranges as a list in same order as PIECE_TYPES
            # typeRanges.append([typeRangesForColor[pt] for pt in PIECE_TYPES])

        numPieces = pieceIndex

        return numPieces, colorRanges, pieceTypeLookup, colorLookup
        # return {
        #     'num pieces': totalNumPieces,
        #     'piece type lookup': pieceTypeLookup,
        #     'piece color lookup': colorLookup
        # }
        # return {
        #     'num pieces': totalNumPieces,
        #     'full range': allPiecesRange,
        #     'color ranges': colorRanges,
        #     'piece type ranges': typeRanges,
        #     'color lookup': colorLookup,
        #     'type lookup': pieceTypeLookup
        # }




    pieces = parse_board_str()

    def create_piece_bitboards(color):
        squares = sum(pieces[color].values(), [])
        return [create_bitboard([square]) for square in squares]

    zobristHashTable = generate_hash_key()
    intitialPieceBitboards = sum(map(create_piece_bitboards, [WHITE,BLACK]),[])
    (numPieces,colorRanges,
     pieceTypeLookup,colorLookup) = setup_piece_indexing(pieces)

    return {
        'initial piece bitboards': intitialPieceBitboards,
        'num pieces': numPieces,
        'color ranges': colorRanges,
        'piece type lookup': pieceTypeLookup,
        'piece color lookup': colorLookup,
        'hash table': zobristHashTable
    }
