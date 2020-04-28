# -*- coding: utf-8 -*-
"""Positional Evaluation"""

import operator

import chess.pregame

class Evaluator:
  """State Evaluator

  A positive score indicates white is winning, while a negative score
  means black is winning. Evaluation features used are Material, Piece
  Square Tables, Center Control, Mobility, Connectivity, Development
  """

  MODES = [LAZY, NORMAL, EAGER] = range(3)

  def __init__(self, mode = LAZY):
    self.mode = mode

    self.pieceSquareTables = chess.pregame.load_piece_square_tables()
    self.masks = chess.pregame.load_evaluation_masks()

    self.pieceValues = (
      1,  # PAWN
      3,  # BISHOP
      3,  # KNIGHT
      5,  # ROOK
      9,  # QUEEN
      0   # KING
    )

    self.weights = (
      50,    # Material
      0.0005,   # Piece Square Table Values
      0.00001,      # development
      5,      # Center Control
      1,      # Connectivity
      3,      # Mobility
      0.2,   # Bishop Pair bonus
      2,     # Pawn structure score
      1,      #pressure
    )

    self.memo = {}

  def __call__(self, state, *args):
    """Main Evaluation function"""

    if state in self.memo:
      return self.memo[state]

    scores = map(lambda f: f(state,*args), self.get_scores())
    dot_product = lambda l1,l2: sum(v1*v2 for v1,v2 in zip(l1,l2))
    valuation = dot_product(scores, self.weights)

    self.memo[state] = valuation

    return valuation

  def score(func):
    """Evaluation Feuture to be used in the Linear Combination"""
    def decorator(self, *args):
      whiteScore = func(self, 0, *args)
      blackScore = func(self, 1, *args)
      return whiteScore - blackScore
    return decorator

  @score
  def material(self, color, state, *args):
    """Piece Value Sum

    Pawn: 1 -- Knight: 3 -- Bishop: 3 -- Rook: 5 -- Queen: 9
    """
    pieces = state.pieces.get_color(color)
    pieceValues = map(lambda p: self.pieceValues[p[1]], pieces)
    return sum(pieceValues)

  @score
  def piece_square_value(self, color, state, *args):
    """Piece-Square Value Sum

    For each piece, a piece square table contains a score for every
    square indicating the strength of a square for that piece.
    """
    pieces =  state.pieces.get_color(color)
    tables = self.pieceSquareTables[color]
    pst_values = map(lambda piece: tables[piece[1]][piece[0]], pieces)
    return sum(pst_values)

  @score
  def development(self, color, state, *args):
    """Piece Development"""
    isPieceDeveloped = lambda mask: mask & state.colors[color] == 0
    return sum(map(isPieceDeveloped, self.masks.minorPieceSquares[color]))

  @score
  def center_control(self, color, state, attacks):
    """Determined by the number of center squares attacked

    Center squares are D4, E4, D5, E5.
    """
    def countCenterSquares(attack):
      isAttackingSquare = lambda square: attack & square != 0
      return sum(map(isAttackingSquare, self.masks.centerSquares))
    return sum(map(countCenterSquares, attacks[color]))

  @score
  def connectivity(self, color, state, attacks):
    """Indicates how well pieces are working together"""
    def countDefences(attack):
      isDefendingPiece = lambda p: p[0] & attack != 0
      return sum(map(isDefendingPiece, state.pieces.get_color(color)))
    return sum(map(countDefences, attacks[color]))

  @score
  def mobility(self, color, state, attacks):
    """Amount of legal moves"""
    pass

  @score
  def king_safety(self, state, attacks, color):
    """TODO"""
    pass

  @score
  def pawn_structure(self, state, attacks, color):
    """TODO"""
    pass

  @score
  def pressure(self, state, attacks, color):
    """TODO"""
    pass


  def get_scores(self):
    """Gets scores used for an evaluation mode

    Modes include Lazy, normal, eager
    """

    # Lazy Evaluation
    yield from (self.material, self.piece_square_value)#, self.center_control)
    if self.mode == Evaluator.LAZY: return

    # Normal Evaluation
    yield from (self.development, self.center_control)
    if self.mode == Evaluator.NORMAL: return

    # Eager Evaluation
    yield from (self.king_safety, self.pawn_structure, self.pressure)
