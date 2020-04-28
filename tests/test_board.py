# -*- coding: utf-8 -*-
"""State, Pieces, and Zobrist Tests"""

from chess import board
from tests.utils import get_random_move

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

def test_zobrist_hashing():
  state = board.create_initial_position()
  for moveCount in range(20):
    hashBeforeMove = hash(state)
    move = get_random_move(state)
    state += move
    state -= move
    assert hash(state) == hashBeforeMove
    state += move
  print('state zobrist hashing test passed')

def test_update():
  pass
