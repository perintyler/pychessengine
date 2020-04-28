# -*- coding: utf-8 -*-
"""Game Tree Search"""

from time import time

import settings
import chess.moves
import chess.board

from debug import *

monitor = SearchMonitor() # Debug Tool
builder = TreeBuilder()   # Debug Tool

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

	monitor.node_searched(depth)

	# only search captures if depth surpassed max depth
	moves = generator.find_moves(state, attacks, attackSets,
								 onlyCaptures = depth > maxDepth)

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
	if depth == maxDepth-1: moves = moves[-10:]
	# if depth == maxDepth-2: moves = moves[-10:]

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

	if beta<=alpha: monitor.cutoff(maximize)

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

	MAX_MOVES = 35

	state = chess.board.create_initial_position()
	generator = chess.moves.Generator()
	evaluator = chess.board.Evaluator()

	movesMade = 0
	while movesMade < MAX_MOVES:
		movesMade += 1
		start = time.time()
		make_best_move(state, evaluator, generator)
		end = time.time()
		print('found move in ' + str(end - start) + ' seconds')

		monitor.print_results()
		monitor.reset()
		# evaluator.debugMode = True
		valuation = evaluator(state, generator.find_attacks(state)[0])
		# evaluator.debugMode  = False
		print('valuation: ' + str(valuation))
		print(state)

def play_against_computer():
	state = chess.board.State.create_initial_position()
	evaluator = chess.board.Evaluator()
	generator = chess.moves.Generator()

	print(state)
	while True:

		def getUserMove():
			def parseUserMove(state):
				ui = input('enter move\n')
				if ui=='q':
					import sys
					sys.exit(0)
				def parseSquare(str):
					file = 'abcdefgh'.index(str[0])
					rank = 8-int(str[1])
					return rank*8 + file
				# try:
				return parseSquare(ui[0:2]), parseSquare(ui[2:4])
				# except:
				# 	print('invalid inputç')
				# 	parseUserMove(state)


			# state = parseUserMove(state, ui)

			start,end = parseUserMove(state)

			foundMove = False
			pieces = []
			for i in range(32):
				p = state.pieces[i]
				loc = get_piece_location(p)
				if loc == start:
					pieces.append(1 << (63-end))
					foundMove = True
				elif loc == end:
					pieces.append(0)
				else:
					pieces.append(p)

			if not foundMove:
				return getUserMove()
			else:
				return chess.board.State(not state.colorToMove, pieces)
		state = getUserMove()
		print(state)

		start = time.time()
		make_best_move(state, evaluator, generator)
		end = time.time()
		print('found move in ' + str(end - start) + ' seconds')

		# monitor.print_results()
		# monitor.reset()
		# evaluator.debugMode = True
		valuation = evaluator(state, generator.find_attacks(state)[0])
		# evaluator.debugMode  = False
		print('valuation: ' + str(valuation))
		print(state)
