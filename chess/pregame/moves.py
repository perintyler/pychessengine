# -*- coding: utf-8 -*-
"""Move Bitboard Generation"""

from chess.pregame.board import get_coordinate,get_square,Bitboard,WHITE,BLACK

PIECE_TYPES = [PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING] = range(6)


class MoveCache:

  def __init__(self, pieceType, find_moves):
    self.pieceType = pieceType
    self.populate(find_moves)

  def populate(self, find_moves):
    squares = range(64)
    moveLists = map(find_moves, squares)
    self.items = list(map(self.create_item, squares, moveLists))

  def create_item(self, square, moves):
    if self.pieceType == PAWN:
      nonAttacks,attacks = moves
      return MoveCache.Item(square, nonAttacks, attacks)
    else:
      return MoveCache.Item(square, moves)

  class Item:
    """Moves for a piece at a square"""

    def __init__(self, startSquare, *endSquareSets):
      self.startSquare = startSquare
      self.endSquareSets = endSquareSets

    @property
    def key(self):
      return Bitboard(self.startSquare)

    @property
    def moves(self):
      allSquares = sum(self.endSquareSets, [])
      return [Bitboard(square) for square in allSquares]

    @property
    def movesets(self):
      bitboards = [Bitboard(*squares) for squares in self.endSquareSets]
      return bitboards[0] if len(self.endSquareSets) == 1 else bitboards

  def get_moves_dict(self):
    return {item.key:item.moves for item in self.items}

  def get_moveset_dict(self):
    return {item.key:item.movesets for item in self.items}

def N(x,y,d=1):  return x,y+d
def E(x,y,d=1):  return x+d,y
def S(x,y,d=1):  return x,y-d
def W(x,y,d=1):  return x-d,y
def NE(x,y,d=1): return x+d,y+d
def SE(x,y,d=1): return x+d,y-d
def SW(x,y,d=1): return x-d,y-d
def NW(x,y,d=1): return x-d,y+d

def get_rays(x,y, directions, numSteps=8):
  makeNSteps = lambda n: [d(x,y,n) for d in directions]
  rays = map(makeNSteps, range(1,numSteps))
  return sum(rays,[])

def get_move_finder(pieceType):

  diagonalsDirections = [NE,SE,SW,NW]
  straightDirections = [N,E,S,W]
  allDirections = [N,NE,E,SE,S,SW,W,NW]

  def get_valid_squares(moves):
    return [get_square(x,y) for x,y in moves if 0<=x<8 and 0<=y<8]

  def find_pawn_moves(square,color):
    # Pawn is the only piece type whos moves depend on its color.
    x,y = get_coordinate(square)
    forward = -1 if color==WHITE else 1
    onStartRank = y == {WHITE: 6, BLACK: 1}[color]
    numSteps = 2 if onStartRank else 1
    moves = [(x, y+step*forward) for step in range(numSteps)]
    attacks = [(x+horizontal, y+forward) for horizontal in [-1,1]]
    return get_valid_squares(moves), get_valid_squares(attacks)

  def find_knight_moves(x,y):
    makeKnightMove = lambda d1,d2: d1(*d2(x,y),2)
    directions = ([(v,h),(h,v)] for v in [N,S] for h in [W,E])
    return [makeKnightMove(d1,d2) for d1,d2 in sum(directions,[])]

  def find_bishop_moves(x,y): return get_rays(x,y,diagonalsDirections)
  def find_rook_moves(x,y):   return get_rays(x,y,straightDirections)
  def find_queen_moves(x,y):  return get_rays(x,y,allDirections)
  def find_king_moves(x,y):   return get_rays(x,y,allDirections,numSteps=1)

  def find_moves(square):
    x,y = get_coordinate(square)
    if   pieceType == KNIGHT: moves = find_knight_moves(x,y)
    elif pieceType == BISHOP: moves = find_bishop_moves(x,y)
    elif pieceType == ROOK:   moves = find_rook_moves(x,y)
    elif pieceType == QUEEN:  moves = find_queen_moves(x,y)
    else:                     moves = find_king_moves(x,y)
    return get_valid_squares(moves)

  if pieceType != PAWN:
    return find_moves
  else:
    def get_white_moves(square): return find_pawn_moves(square, WHITE)
    def get_black_moves(square): return find_pawn_moves(square, BLACK)
    return get_white_moves, get_black_moves

def generate_move_cache():
  moveCaches,movesetCaches = [],[]
  for pieceType in PIECE_TYPES:
    find_moves = get_move_finder(pieceType)
    if pieceType == PAWN:
      caches = [MoveCache(PAWN, find_moves[color]) for color in range(2)]
      moveCaches.append([cache.get_moves_dict() for cache in caches])
      movesetCaches.append([cache.get_moveset_dict() for cache in caches])
    else:
      cache = MoveCache(pieceType, find_moves)
      moveCaches.append(cache.get_moves_dict())
      movesetCaches.append(cache.get_moveset_dict())

  return {
    'moves': moveCaches,
    'move sets': movesetCaches
  }
