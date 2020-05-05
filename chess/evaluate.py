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

  def __init__(self):

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
      1.5,    # Material
      0.001,   # Piece Square Table Values
      1,      # development
      0.3,      # Center Control
      0.02,   # tempo bonus
      5,      # Connectivity
      3,      # Mobility
      0.2,   # Bishop Pair bonus
      2,     # Pawn structure score
      1,      #pressure
    )

    self.memo = [{} for _ in range(len(Evaluator.MODES))]

  def __call__(self, state, *args, mode=NORMAL):
    """Main Evaluation function"""

    if state.hash in self.memo[mode]:
      return self.memo[mode][state.hash]


    scores = [score(state,*args) for score in self.get_scores(mode)]
    dot_product = lambda l1,l2: sum(v1*v2 for v1,v2 in zip(l1,l2))
    valuation = dot_product(scores, self.weights)
    self.memo[mode][state.hash] = valuation

    # if mode == 1:
    #   print('_'*10)
    #   print(state)
    #
    #   print('scores', list(scores))
    #   print('weighted', [v1*v2 for v1,v2 in zip(scores, self.weights)])
    #   print('valuation:',valuation)
    #   print('_'*10)

    return valuation

  def score(func):
    """Evaluation Feuture to be used in the Linear Combination"""
    def decorator(self, *args):
      whiteScore = func(self, 0, *args)
      blackScore = func(self, 1, *args)
      return round(whiteScore - blackScore, 4)
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
    return sum(pst_values) / state.pieces.size(color)

  @score
  def development(self, color, state, *args):
    """Piece Development"""
    isPieceDeveloped = lambda mask: mask & state.colors[color] == 0
    developmentMap = map(isPieceDeveloped, self.masks.minorPieceSquares[color])
    return sum(developmentMap) / 4 # 4 minor pieces per color


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
    defenceBoolMap = map(countDefences, attacks[color])
    return sum(defenceBoolMap) / state.pieces.size(color)

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

  @score
  def tempo(self, color, state, *args):
    """Bonus for the moving player

    The purpose of a tempo bonus is to discourage cyclical repetitions.
    """
    return int(state.colorToMove == color)

  def get_scores(self, mode):
    """Gets scores used for an evaluation mode

    Modes include Lazy, normal, eager
    """

    # Lazy Evaluation
    yield from (self.material, self.piece_square_value)
    if mode == 0: return

    # Normal Evaluation
    yield from (self.development, self.center_control, self.tempo)#, self.connectivity)
    if mode == 1: return

    # Eager Evaluation
    yield from (self.mobility, self.king_safety, self.connectivity, self.king_safety, self.pawn_structure, self.pressure)
