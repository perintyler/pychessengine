# -*- coding: utf-8 -*-
"""Game Tree Search"""

from time import time

import settings
import chess.moves
import chess.board

# from debug import *

# monitor = SearchMonitor() # Debug Tool
# builder = TreeBuilder()   # Debug Tool

MAX_VALUE = 1000

def explore_leaves(state, evaluator, generator,
           maximize, alpha, beta, depth,
           maxDepth, maxValue, isQuiet=True):
  """Minimax Alpha-Beta Search

  This recursive function preforms a depth first tree search. The nodes
  on the tree are represented as a board State object, and the edges on the
  tree are represented as moves.

  The root state node is never copied, but rather, it is updated and passed
  on to searches of the children nodes. When the max search depth is reached,
  the leaves are evaluated and compared, and then the moves are reverted as
  the recursive calls collapse.
  """

  attacks,attackSets = generator.find_attacks(state)

  # recursive base case. Leaf has been reached. Return its valuation.
  if depth >= maxDepth and isQuiet:
    return evaluator(state, attacks)

  # monitor.node_searched(depth)

  # only search captures if depth surpassed max depth
  moves = generator.find_moves(state, attacks, attackSets)
                               #onlyCaptures = depth > maxDepth and not isQuiet)

  if len(moves) == 0:
    assert depth > maxDepth
    return evaluator(state, attacks)

  # sorting moves everytime seems to speed things up
  moveOrder = []
  while len(moves) > 0:
    m = moves.pop()
    state+=m
    v = evaluator(state,attacks)
    moveOrder.append((v,m))
    state-=m
  moves = sorted(moveOrder, key=lambda x:x[0], reverse=state.colorToMove==1)
  moves = [m[1] for m in moves]

  # beam search
  if depth == maxDepth-2: moves = moves[-10:]
  if depth >= maxDepth: moves = moves[-5:]

  # initilize best as worst value
  best = -maxValue if maximize else maxValue
  bestMove = None

  # search edges until alpha/beta cutoff occurs
  while beta > alpha and len(moves) > 0:

    # get the highest priority move from the move queue
    move = moves.pop()

    # get child node by updating state
    state += move

    # make recursive call to perform depth first search
    value = explore_leaves(state, evaluator, generator,
                           not maximize, alpha, beta,
                           depth+1, maxDepth, maxValue,
                           isQuiet = move.captureType is None)
    # revert state
    state -= move

    # maximize white and minimize black
    if maximize:
      best = max(value, best)
      alpha = max(alpha, best)
      bestMove = move
    else:
      best = min(value, best)
      beta = min(beta,best)
      bestMove = move

  # if beta<=alpha: monitor.cutoff(maximize)

  # if depth is 0, the search is complete
  return bestMove if depth == 0 else best

def make_best_move(state, evaluator, generator):
  alpha,beta = -MAX_VALUE,MAX_VALUE
  maximizeRoot = not state.colorToMove # maximize white
  depth,maxDepth = 0,settings.SEARCH_DEPTH

  bestMove = explore_leaves(state, evaluator, generator,
                            maximizeRoot, alpha, beta,
                            depth, maxDepth, MAX_VALUE)
  state += bestMove

def play_computer_game():
  import time
  MAX_MOVES = 35

  state = chess.board.create_initial_position()
  generator = chess.moves.Generator()
  evaluator = chess.board.Evaluator()
  print(state)
  movesMade = 0
  while movesMade < MAX_MOVES:
    movesMade += 1
    start = time.time()
    make_best_move(state, evaluator, generator)
    end = time.time()
    print('found move in ' + str(end - start) + ' seconds')

    # monitor.print_results()
    # monitor.reset()
    valuation = evaluator(state, generator.find_attacks(state)[0])
    print('valuation: ' + str(valuation))
    print(state)

def play_against_computer(): pass
