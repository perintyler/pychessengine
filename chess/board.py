# -*- coding: utf-8 -*-
"""Board Representation"""

from collections import namedtuple, deque
from functools import reduce
import operator

from chess.evaluate import Evaluator # for visibility/readibility
from settings import PIECE_REPRESENTATION
import chess.pregame

class InvalidPieceOperation(Exception): pass
class PieceNotFoundException(Exception): pass

class PieceSet(list):
  """Piece List Representation

  Includes functionality for piece iteration, update, insert, and remove.
  Pieces will always be stored in the same index for any given board state.
  When a piece is captured, its index will store as an empty bitboard. This
  allows for fast piece type lookup and iteration.
  """

  def __init__(self, *args):
    list.__init__(self, *args)

    # self.emptySlots = deque()

    (self.numPieces,
     self.typeLookup,
     self.colorLookup,
     self.colorRanges) = chess.pregame.load_piece_index_values()

    self.colorCounts = [end-start for start,end in self.colorRanges]

  def __iter__(self):
    """Iterates each piece's bitboard, color, and type.

    Captured pieces, which are set to zero, are skipped.
    """
    for index in range(self.numPieces):
      piece = self[index]
      if piece == 0: continue
      pieceType = self.typeLookup[index]
      pieceColor = self.colorLookup[index]
      yield piece, pieceType, pieceColor

  def update(self, p0, p1, color):
    """Updates a piece"""
    start,end = self.colorRanges[color]
    for index in range(start,end):
      piece = self[index]
      if piece == p0:
        self[index] = p1
        return self.typeLookup[index]
    raise InvalidPieceOperation(f'cannot update piece')

  def insert(self, piece, pieceType, color):
    """Inserts a piece by finding an empty slot"""
    self.colorCounts[color] += 1
    start,end = self.colorRanges[color]
    for index in range(start,end):
      # slot must be empty and the index must be for
      # the correct type of the piece to be inserted
      indexCanStorePiece = self[index] == 0 \
                       and self.typeLookup[index]  == pieceType \
                       and self.colorLookup[index] == color

      if indexCanStorePiece:
        self[index] = piece
        return
    raise InvalidPieceOperation(f'cannot insert piece')

  def remove(self, piece, color):
    """Removes a piece by setting its value equal to 0"""
    self.colorCounts[color] -= 1
    start,end = self.colorRanges[color]
    for index in range(start,end):
      if self[index] == piece:
        self[index] = 0
        # self.emptySlots.add(index)
        return self.typeLookup[index]
    raise InvalidStateUpdateException(f'cannot remove piece')

  def get_color(self, color):
    """Returns all pieces of the given color"""
    start,stop = self.colorRanges[color]
    for index in range(start,stop):
      piece = self[index]
      if piece == 0: continue
      yield piece,self.typeLookup[index]

  def size(self, color):
    return self.colorCounts[color]

class State:
  """Board Representation

  Can be updated with moves backwards and forwards. Impements Zobrist
  hashing. State properties: PieceSet and occupancy bitboards (for all
  pieces, for each color, and for each piece type). Printing it will
  print a formatted board string.
  """

  def __init__(self, colorToMove, pieces):
    self.colorToMove = colorToMove
    self.pieces = PieceSet(pieces)

    # occupancy bitboards
    self.pieceTypes = [0]*6 # 6 types: pawn,knight,bishop,rook,queen,king
    self.colors = [0]*2   # 2 colors: white, black
    self.occupied = 0     # all pieces

    # fill occupancy bitboards with pieces
    for piece, pieceType, pieceColor in self.pieces:
      self.pieceTypes[pieceType] |= piece
      self.colors[pieceColor] |= piece
      self.occupied |= piece

    # load zobrist table from file then compute initial hash value
    self.hashTable = chess.pregame.load_hash_values()
    pieceHashValues = map(self.hashTable.__getitem__, self.pieces)
    self.hash = reduce(operator.xor, pieceHashValues, 0)
    self.history = []

  def __add__(self, move):
    """Applies a move"""
    self.history.append(move)
    return self._update(move)

  def __sub__(self, move):
    """Reverts a move"""
    self.history.pop()
    return self._update(move, reverse=True)

  def _update(self, move, reverse=False):
    """Helper. Should not be called directly."""

    # define old/updated piece and moving color depending on move direction
    p0,p1 = (move.end,move.start) if reverse else (move.start,move.end)
    color = not self.colorToMove if reverse else self.colorToMove

    # update piece set
    self.pieces.update(p0, p1, color)

    # Bitwise subtract the old piece from occupancy bitboards
    self.pieceTypes[move.pieceType] &= ~p0
    self.colors[color] &= ~p0

    # Bitwise union the updated piece from occupancy bitboards.
    self.pieceTypes[move.pieceType] |= p1
    self.colors[color] |= p1

    moveIsACapture = move.captureType is not None
    if reverse and moveIsACapture:
      # reversed capture, insert captured piece back into piece set.
      self.pieces.insert(p0, move.captureType, not color)
      self.pieceTypes[move.captureType] |= p0
      self.colors[not color] |= p0
    elif moveIsACapture:
      # forward capture: remove captured piece from piece set
      self.pieces.remove(p1, not color)
      self.colors[not color] &= ~p1

      # subtract piece from pieceType occupancy bitboard unless
      # the piece captured a piece of the same type
      if move.pieceType != move.captureType:
        self.pieceTypes[move.captureType] &= ~p1

    # update board occupation with updated color bitboards
    self.occupied = self.colors[0] | self.colors[1]

    # update zobrist hash by XORing in/out the old/updated piece
    self.update_hash(p0, p1, color, move.pieceType, move.captureType, reverse)
    self.hash ^= 0xF8D626AAAF278509

    # update turn
    self.colorToMove = not self.colorToMove

    return self

  def update_hash(self, pieceIn, pieceOut, color,
                  movedPieceType, removedPieceType, reverse):
    """Rolling Zobrist Hash"""

    # XOR out the piece bitboard before move
    self.hash ^= self.hashTable[(pieceOut, movedPieceType, color)]

    # XOR in the updated piece
    self.hash ^= self.hashTable[(pieceIn, movedPieceType, color)]

    # if move was a capture, XOR out captured piece
    if removedPieceType is not None:
      removedPiece = pieceOut if reverse else pieceIn
      self.hash ^= self.hashTable[(removedPiece, removedPieceType, not color)]

  def get_piece_type(self, piece):
    """Finds the given piece and returns its type"""
    for pieceType, pieceSet in enumerate(self.pieceTypes):
      if piece & pieceSet != 0:
        return pieceType
    raise PieceNotFoundException('Could not find piece type')

  def __str__(self):
    """Returns a formatted board string"""
    squares = ['.']*64 # empty square represented as '.'
    for piece,pieceType,color in self.pieces:
      isBitOn = lambda index: piece & (1 << (63-index)) != 0
      square = list(map(isBitOn, range(64))).index(True)
      squares[square] = PIECE_REPRESENTATION[color][pieceType]
    formatRow = lambda r: '87654321'[r//8] + ' '.join(squares[r:r+8])
    rows = map(formatRow, range(0,64,8))
    return '\n'.join(map(formatRow, range(0,64,8))) + '\n a b c d e f g h'

def create_initial_position():
  """Returns initial State, which can be configured in settings.py"""
  return State(0, chess.pregame.load_initial_pieces())

#################################################################
# PGN PARSING: IN PROGRESS                                 #
#################################################################

testPgn = '''
[Event "F/S Return Match"]
[Site "Belgrade, Serbia JUG"]
[Date "1992.11.04"]
[Round "29"]
[White "Fischer, Robert J."]
[Black "Spassky, Boris V."]
[Result "1/2-1/2"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 {This opening is called the Ruy Lopez.}
4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7
11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5
Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6
23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5
hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5
35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6
Nf2 42. g4 Bd3 43. Re6 1/2-1/2
'''

import re

# https://hub.gke.mybinder.org/user/ipython-ipython-in-depth-kjx9okko/notebooks/binder/pgnparsework.ipynb
def parse_pgn(pgn):
  # parse headers
  headers = re.findall('\[.*\]',pgn)

  # remove headers
  pgn = re.sub('\[.*\]', '', pgn)

  # remove notes
  pgn = re.sub('\{.*\}', '', pgn).lstrip()

  pgn = pgn = re.sub('\n',' ', pgn.lstrip())

  match = '\d+\. (?:O-O|[a-zA-Z]+\d\+?) (?:O-O|[a-zA-Z]+\d\+?|1/2-1/2|1-0|0-1)'
  turns = re.findall(match,pgn)
  for turn in turns:
    moveInfo,whiteMoveStr,blackMoveStr = moveStr.split(' ')

    moveNumber = moveInfo[0:moveInfo[0].index('.')]


  return pgn
