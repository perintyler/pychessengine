# -*- coding: utf-8 -*-
"""Board Setup

Generates Initial Piece Bitboards, Piece Index Values (see chess/board.py),
and Zobrist hash key
"""

WHITE = 0
BLACK = 1

def Bitboard(*squares):
  """Bitboard factory"""
  bits = 0
  for square in squares:
    squareMask = 1 << (63-square)
    bits |= squareMask
  return bits

def reverse_bitboard(bitboard):
  """Binary Reversal"""
  reversedBits = 0
  for _ in range(64):
    reversedBits <<= 1
    reversedBits |= bitboard & 1
    bitboard >>= 1
  return reversedBits

def count_bits(bitboard):
  """Population Count"""
  count = 0
  while(bitboard):
    bitboard &= bitboard - 1
    count += 1
  return count

def get_squares_from_bitboard(bitboard):
    """returns on bits starting with least significant bit"""
    squares = []
    for squareIndex in range(63,0,-1):
        if bitboard & 1:
            squares.append(squareIndex)
        bitboard >>= 1
    return squares

def get_square(x,y):
  """board index: 0-63"""
  return 8*y + x

def get_coordinate(square):
  """file,rank"""
  x = square%8
  y = int((square-x)/8)
  return x,y

def parse_notation(notation):
  """"""
  file = 'ABCDEFGH'.index(notation[0])
  rank = 8-int(notation[1])
  return rank*8 + file

def generate_hash_table():
  """
  Precomputes all Zobrist Hash Table Values for quick lookup

  Random bitstrings for  each piece element
  """
  from data.config.hash_key import RANDOM_ARRAY
  hashes = {}
  for square in range(64):
    piece = Bitboard(square)
    for pieceType in range(6):
      for color in range(2):
        colorMultiplier = 64 if color==0 else 64*2
        tableIndex = colorMultiplier*(pieceType+1) + square - 64
        hashes[(piece,pieceType,color)] = RANDOM_ARRAY[tableIndex]
  return hashes

def setup_pieces():
  """"""

  def parse_pieces_from_board_configuration():
    from settings import INITIAL_POSITION

    # For invalid chars in board str array
    class InvalidInitialPositionException(Exception): pass


    chars = ('p','n','b','r','q','k')
    charPieceTypeDict = {c:pieceType for c,pieceType in zip(chars,range(6))}

    # create initially empty piece type dicts for white/black
    pieces = {
      WHITE: {pieceType:[] for pieceType in range(6)},
      BLACK: {pieceType:[] for pieceType in range(6)}
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

    colorRanges, colorLookup, pieceTypeLookup = [],[],[]

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

    return {
      'num pieces': pieceIndex,
      'color ranges': colorRanges,
      'piece type lookup': pieceTypeLookup,
      'piece color lookup': colorLookup,
    }

  def create_piece_bitboards(pieces):
    whitePieces,blackPieces = [sum(pieces[c].values(),[]) for c in range(2)]
    pieces = whitePieces + blackPieces
    return [Bitboard(piece) for piece in pieces]

  def create_piece_square_table_lookup():
    """PST"""
    import json
    with open('data/config/pst.json') as f:
      pstConfig = json.load(f)

    PIECE_SQUARE_TABLES = pstConfig['pst']
    whiteLookups,blackLookups = [],[]
    for table in PIECE_SQUARE_TABLES:

      whiteLookupForPiece,blackLookupForPiece = {},{}
      for square in range(64):
        squareBitboard = Bitboard(square)
        # tables are upside down for black. Flip the y value
        x,y = get_coordinate(square)
        flippedSquare = get_square(x,7-y)
        flippedSquareBitboard = Bitboard(flippedSquare)
        whiteLookupForPiece[flippedSquareBitboard] = table[square]
        blackLookupForPiece[squareBitboard] = table[square]

      whiteLookups.append(whiteLookupForPiece)
      blackLookups.append(blackLookupForPiece)

    return [whiteLookups,blackLookups]

  pieces = parse_pieces_from_board_configuration()

  return {
    'initial pieces': create_piece_bitboards(pieces),
    'piece index values': setup_piece_indexing(pieces),
    'pst': create_piece_square_table_lookup(),
  }

def generate_board_data():
  return {**setup_pieces(), 'hash values': generate_hash_table()}
