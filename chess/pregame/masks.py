# -*- coding: utf-8 -*-
"""Bitboard Mask Generation"""

from chess.pregame.board import (Bitboard, reverse_bitboard, parse_notation,
                 get_square, get_coordinate)

# ordered top right to bottom left
DIAGONAL_MASK_LIST = [
  0x8000000000000000,
  0x4080000000000000,
  0x2040800000000000,
  0x1020408000000000,
  0x810204080000000,
  0x408102040800000,
  0x204081020408000,
  0x102040810204080,
  0x1020408102040,
  0x10204081020,
  0x102040810,
  0x1020408,
  0x10204,
  0x102,
  0x1,
]

# ordered top left to bottom right
ANTI_DIAGONAL_MASK_LIST = [
  0x100000000000000,
  0x201000000000000,
  0x402010000000000,
  0x804020100000000,
  0x1008040201000000,
  0x2010080402010000,
  0x4020100804020100,
  0x8040201008040201,
  0x80402010080402,
  0x804020100804,
  0x8040201008,
  0x80402010,
  0x804020,
  0x8040,
  0x80,
]

def create_mask(*squareNotationList):
  return Bitboard(*map(parse_notation,squareNotationList))

def generate_ray_masks(reverse=False):
  """Generates file, rank, diagonal, and antidiagonal masks

  Example Diagonal Mask       Example Antidiagonal Mask

    00000010                        10000000
    00000100                        01000000
    00001000                        00100000
    00100000                        00010000
    01000000                        00001000
    10000000                        00000100
    00000000                        00000010
    00000000                        00000001

  Example File Mask               Example Rank Mask

    00000010                        00000000
    00000010                        11111111
    00000010                        00000000
    00000010                        00000000
    00000010                        00000000
    00000010                        00000000
    00000010                        00000000
    00000010                        00000000
  """
  # create a mask for each rank
  rankMaskList = []
  for rank in range(8):
    rankStartIndex = rank*8
    rankSquares = range(rankStartIndex,rankStartIndex+8)
    rankMask = Bitboard(*rankSquares)
    rankMaskList.append(rankMask)

  # create a mask for each file
  fileMaskList = []
  for file in range(8):
    fileSquares = range(file,64,8)
    fileMask = Bitboard(*fileSquares)
    fileMaskList.append(fileMask)

  maskLists = [rankMaskList, fileMaskList,
               DIAGONAL_MASK_LIST, ANTI_DIAGONAL_MASK_LIST]

  # iterate through each square on the board and add the rank, file,
  # diagonal, and antidiagonal masks that the square is a part of. This
  # way, a square's mask index does not need to be computed for retreival
  maskDicts = (rankMasks,
               fileMasks,
               diagonalMasks,
               antiDiagonalMasks) = {},{},{},{}

  for square in range(64):
    fileIndex,rankIndex = get_coordinate(square)
    diagonalIndex = (square // 8) + (square % 8)
    antiDiagonalIndex = (square // 8) + 7 - (square % 8)
    maskIndecies = [rankIndex, fileIndex, diagonalIndex, antiDiagonalIndex]

    for dict,list,index in zip(maskDicts, maskLists, maskIndecies):
      mask = list[index]
      if reverse:
        dict[Bitboard(square)] = reverse_bitboard(mask)
      else:
        dict[Bitboard(square)] = mask

  labels = ['ranks', 'files', 'diagonals', 'antidiagonals']
  if reverse: labels = ['reversed' + label.title() for label in labels]

  return {label: masks for label, masks in zip(labels, maskDicts)}

def generate_reversed_square_masks():
  reversedSquares = {}
  for square in range(64):
    squareBitboard = Bitboard(square)
    reversedSquares[squareBitboard] = reverse_bitboard(squareBitboard)
  return reversedSquares

def generate_pawn_blocker_masks():
  """Mask to get the square directly in front of a pawn"""
  def create_blocker(square, direction):
    x,y = get_coordinate(square)
    blockerSquare = get_square(x,y+direction)
    return Bitboard(blockerSquare) if 0<=blockerSquare<64 else 0

  whiteMasks,blackMasks = {},{}
  for square in range(64):
    squareBitboard = Bitboard(square)
    whiteMasks[squareBitboard] = create_blocker(square,-1)
    blackMasks[squareBitboard] = create_blocker(square,1)

  return whiteMasks,blackMasks

def generate_center_file_masks():
  fileMasks = generate_ray_masks()['files']
  return fileMasks[Bitboard(3)],fileMasks[Bitboard(4)]

def generate_center_square_masks():
  """TODO: add example"""
  centerSquares = ('E4', 'D4', 'E5', 'D5')
  return list(map(create_mask, centerSquares))

def generate_minor_piece_mask():
  """Development mask

  Minor Pieces: knight, bishop


  White Minor piece masks  Black Minor piece masks
        00000000                0XX00XX0
        00000000                00000000
        00000000                00000000
        00000000                00000000
        00000000                00000000
        00000000                00000000
        00000000                00000000
        0XX00XX0                00000000
  """
  whitePieceMasks = map(create_mask,['B1', 'C1', 'F1', 'G1'])
  blackPieceMasks = map(create_mask,['B8', 'C8', 'F8', 'G8'])
  return list(whitePieceMasks), list(blackPieceMasks)

def generate_castle_masks():
  """Generates a bitboard for castle square for each castle type

            Each square marked by an x gets its own mask.

                              00000000
                              00000000
                              00000000
                              000XX000
                              000XX000
                              00000000
                              00000000
                              00000000
 """
  castleSquares = (
    ['D1', 'C1', 'B1'], # QUEENSIDE WHITE
    ['D8', 'C8', 'B8'], # QUEENSIDE BLACK
    ['F1', 'G1'],     # KINGSIDE WHITE
    ['F8', 'G8']      # KINGSIDE BLACK
  )
  castleMasks = [create_mask(*squares) for squares in castleSquares]

  return { 'queenside': castleMasks[0:2], 'kingside': castleMasks[2:4] }

def create_king_attack_zone_masks():
  pass
  
def generate_masks():
  return {
    **generate_ray_masks(),
    **generate_ray_masks(reverse=True),
    'reversedSquares':   generate_reversed_square_masks(),
    'pawnBlockers':      generate_pawn_blocker_masks(),
    'centerSquares':     generate_center_square_masks(),
    'centerFiles':       generate_center_file_masks(),
    'castleSquares':     generate_castle_masks(),
    'minorPieceSquares': generate_minor_piece_mask()
  }
