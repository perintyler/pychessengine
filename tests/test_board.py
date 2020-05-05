# -*- coding: utf-8 -*-
"""State, Pieces, and Zobrist Tests"""

from chess import board
from tests.utils import get_random_move, get_all_moves

def test_occupancy_bitboards():
  state = board.create_initial_position()
  for moveCount in range(20):
    for piece,pieceType,color in state.pieces:
      # test piece type occupancy
      for pt,occupancy in enumerate(state.pieceTypes):
        if pt == pieceType:
          assert occupancy & piece != 0
        else:
          assert occupancy & piece == 0

      # test color occupancy
      assert state.colors[color] & piece != 0
      assert state.colors[not color] & piece == 0

      # test all piece occupancy
      assert state.occupied & piece != 0

    state += get_random_move(state)
  print('state occupancy bitboard test passed')

def test_piece_set():
  state = board.create_initial_position()

  def check_for_doubles():
    pieces = set()
    for piece,pieceType,color in state.pieces:
      assert piece not in pieces
      pieces.add(piece)

  for _ in range(30):
    check_for_doubles()
    state += get_random_move(state)
  while state.history:
    check_for_doubles()
    state -= state.history[-1]
  print('piece set test passed')

def test_zobrist_hashing():
  hashes = {}
  state = board.create_initial_position()
  for moveCount in range(30):
    moves = get_all_moves(state)
    for move in moves:
      hashBeforeMove = state.hash
      state += move
      if state in hashes:
        assert hashes[state.hash] == (str(state),state.colorToMove)
      else:
        hashes[state.hash] = (str(state),state.colorToMove)
      state -= move
      assert state.hash == hashBeforeMove
    state += get_random_move(state)

  print('state zobrist hashing test passed')

def test_update():
  pass
