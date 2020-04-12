# -*- coding: utf-8 -*-
""" Best Move Search

# TODO:
- move hash to board.py
- get rid of position/tree
- https://www.chessprogramming.org/Iterative_Deepening
"""
from data.hash_key import RANDOM_ARRAY as ZOBRIST_HASH_TABLE
from chess import move, PositionEvaluator, board
from debug_tools import *

# from chess import board
# from chess import move

# from chess.evaluate import Evaluator

NODE_TYPES = (
	PRINCIPLE_VARIATION,
	FAIL_HIGH,
	FAIL_LOW
) = range(3)

SEARCH_DEPTH = 3
#
# class Position:
# 	'''Search Node'''
#
# 	def __init__(self, state, depth, isQuiet=True):
# 		self.state = state
# 		self.depth = depth
# 		self.isNull = False
# 		self.generator = MovesGenerator(state)
# 		self.evaluator = chess.PositionEvaluator()
# 		self.valuation = None
# 		self.moves = None
# 		# quiet positions did not from capture
# 		self.isQuiet = isQuiet
# 		self.maximize = self.state.colorToMove == WHITE
#
# 	@property
# 	def edges(self):
# 		yield from self.generator.find_moves(self.state)
#
# 	@property
# 	def children(self):
# 		'''Generates all possible positions resulting from legal moves'''
# 		nextPositions = []
# 		for move in self.edges:
# 			pieces = self.state.serialize(move)
#
# 			updatedBoard = board.State(not self.state.colorToMove, pieces)
# 			nextPositions.append(Position(updatedBoard,self.depth+1))
# 		return nextPositions
#
# 	def evaluate(self):
# 		# self.evaluater.process_pieces(self.state.get_pieces())
# 		self.valuation = self.evaluator(self.state, self.generator.moves)
#
# 	def __repr__(self):
# 		return f'<Position: valuation: {self.valuation} depth: {self.depth}>'
#
# 	# define comparison operators using the positions valuation
# 	def __lt__(self, other): return self.valuation < other.valuation
# 	def __le__(self, other): return self.valuation <= other.valuation
# 	def __gt__(self, other): return self.valuation > other.valuation
# 	def __ge__(self, other): return self.valuation >= other.valuation
# 	def __eq__(self, other): return self.valuation == other.valuation
#
#
# class NullPositionSearchedError(Exception): pass
#
# class NullPosition(Position):
#
# 	def __init__(self, maximize):
# 		self.valuation = float('-inf' if maximize else 'inf')
# 		self.isNull = True
#
# 	def get_next(self): raise NullPositionSearchedError('null children')
#
# 	def evaluate(self): raise NullPositionSearchedError('null evaluation')

monitor = SearchMonitor()

class MoveQueue:
	"""Priority Queue"""
	def __init__(self): pass

class Node:

	def __init__(self, value):
		self.value = value

	@property
	def edges(self):
		pass

	@property
	def children(self):
		pass


# check for alpha-beta cutoff. If alpha is greater than beta,
# the opponents optimal worst outcome is better than own optimal
# worst outcome. The branch is guaranteed to be suboptimal and
# should not be searched any deeper.
def minimax(maximize, state, alpha, beta, depth, maxDepth, firstMove=None):
	""" todo pass move generator and position evaluator in parameters so
	moves and evaluations can be updated, non computed from scratch"""
	# recursive base case: max depth reached
	if depth >= maxDepth:
		# print('\n'.join(['-'*10,'evaluation: ' + str(val),str(state),'-'*10]))
		return PositionEvaluator()(state)
	# print(f'alpha,beta: ({alpha.valuation},{beta.valuation})')
	monitor.node_searched(depth)
	bestValue = float('-inf') if maximize else float('inf')
	generator = move.Generator(state)
	for edge in generator.find_moves(state):
		if depth == 0: firstMove = edge

		child = board.State(not state.colorToMove, state.serialize(edge))

		# print('\n'.join(['-'*10,str(child),'-'*10]))
		# recursively call minimax on the child before comparing
		# it to its siblings to perform depth first search
		value = minimax(not maximize,
					    child, alpha, beta,
					   	depth+1, maxDepth,
					   	firstMove)

		if maximize:
			bestValue = max(value, bestValue)
			alpha = max(alpha, bestValue)
			if beta<=alpha:
				monitor.alpha_cutoff()
				break
		else:
			bestValue = min(value, bestValue)
			beta = min(beta,bestValue)
			if beta<=alpha:
				monitor.beta_cutoff()
				break
	return firstMove if depth == 0 else bestValue

class Tree:
	'''Decision Tree'''

	def __init__(self,root,maxSearchDepth=5):
		# crawl
		self.root = root
		self.maxSearchDepth = maxSearchDepth

	def explore_leaves(self):
		alpha = float('-inf')
		beta = float('inf')
		firstMove = None
		rootValue = PositionEvaluator()(self.root)
		rootDepth = 0
		maximizeRoot = self.root.colorToMove == 0 # maximize white

		bestMove = minimax(maximizeRoot,
						   self.root, alpha, beta,
						   rootDepth, self.maxSearchDepth)

		print('best move')
		monitor.print_results()
		newColor = not self.root.colorToMove
		return board.State(newColor, self.root.serialize(bestMove))


def for_best_move(boardState):
	return Tree(boardState).explore_leaves()

class Hash:
	'''Zobrist Hash'''

	def __init__(self):
		self.memo = {}

	def contains(self, state):
		pass

	def add(self, state, valuation, moves):
		pass

	def update_hash_value(self, previousStateHash, move,
						   movedPieceType, removedPieceType):

		boardHash = previousStateHash
		colorOut = not state.colorToMove
		# XOR out the previous piece
		boardHash ^= ZOBRIST_HASH_TABLE[self.get_piece_hash_index(move.startSquare,
														 	  movedPieceType,
														 	  colorOut)]
		'''colors may be wrong here'''
		# XOR in the updated piece
		boardHash ^= ZOBRIST_HASH_TABLE[self.get_hash_index(move.endSquare,
													   	movedPieceType,
													   	colorOut)]

		# if move was a capture, XOR out captured piece
		if removedPieceType is not None:
			boardHash ^= ZOBRIST_HASH_TABLE[self.get_hash_index(piece.endSquare,
															removedPieceType,
															state.colorToMove)]

		return boardHash

	def compute_hash_value(self, state):
		'''initial  hash'''
		boardHash = 0
		for piece, pieceType, color in state.pieces.all:
			if piece == 0: continue
			pieceIndex = self.get_piece_hash_index(piece,pieceType,color)
			boardHash ^= ZOBRIST_VALUES[pieceIndex]
		return boardHash

	def get_hash_index(self, piece, pieceType, pieceColor):
		pieceIndex = pieceType+1
		pieceTypeMultiplier = 64 if color==WHITE else 64*2
		squareForPiece = SQUARE_LOOKUP[piece]
		return pieceTypeMultiplier*pieceType + squareForPiece




# class Tree:
# 	''' Decision Tree '''
#
# 	def __init__(self, board, maxSearchDepth=3):
# 		self.root = Position(board, 0)
# 		self.cutoffs = 0
# 		self.leavesSearched = 0
# 		self.maxSearchDepth = maxSearchDepth
#
# 	def get_max_depth(self):
# 		return self.root.depth + self.maxSearchDepth
#
# 	def get_best_move(self):
# 		# initial search values (alpha: -inf, beta: inf)
# 		maximizeRoot = self.root.state.colorToMove == WHITE
# 		alpha = NullPosition(True) # -inf
# 		beta = NullPosition(False) # inf
# 		maxDepth = self.get_max_depth()
# 		# call the minimax function
# 		bestPosition = minimax(self.root, alpha, beta, maximizeRoot, maxDepth, None)
# 		self.root = bestPosition
# 		monitor.print_results()
# 		print(zobrist)
		# assert optimalLeaf.board.colorToMove == WHITE
		# The optimal leaf is a decendant of the position created by the
		# best move. To get optimal position, iterate backwards through tree
		# optimalPosition = optimalLeaf.get_ancestor(self.root.depth+1)
		# print('leaf color: ' + str(optimalLeaf.board.colorToMove))
		# before returning the board of the optimal position, update
		# root allowing for subsequent calls to get next best position
		# self.update_root(optimalPosition)
		# return optimalPosition.lastMove, optimalPosition.board
		# return bestPosition.state

	# def update_with_move(self, move):
	# 	if self.root.children is None:
	# 		self.root.create_children()
	# 	for child in self.root.children:
	# 		lastMove = child.lastMove
	# 		sameStart = move.piece.square == lastMove.piece.square
	# 		sameDest = move.endSquare == lastMove.endSquare
	# 		if sameStart and sameDest:
	# 			self.update_root(child)
	# 			return self.root.board
	# 	assert False

	# def printValueTemps(self):
	# 	bleh = ['Material','PST','Center Control','Connectivity','Mobility','Bishop Pair Bonus', 'Pawn Structure', 'Development','Pressure']

	# 	printStr = 'valuation: ' + str(self.root.valuation) + '\n'
	# 	for v,c,b in zip(self.root.valueTemps, CONSTANTS, bleh):
	# 		score = v*c
	# 		# printStr += f'\t{b}: {score}\n'
	# 		printStr += '\t' + str(b) + ': ' + str(score) + '\n'
	# 	print(printStr)
