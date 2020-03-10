# search.py
# --------------------------------------------------------------- 
# This file can be used to create a search tree that finds a
# player's best available move. Each node in the tree represents
# a position, and each edge represents a move. The optimal move
# is determine by minimizing loss using a minimax algorithm with
# alpha-beta pruning, which is implemented in minimax.py.
# The initial search has the most responsibility becaues it
# requires constructing N layers of the tree, where N is equal
# to the search depth. After each search, the root moves along
# the optimal move edge, becoming one of its children. This chops
# off the top layer of the tree, resulting in a tree with height
# equal to search depth minus 1. Therefore, subsequent searches
# only need to construct 1 more layer of the tree. To compensate
# for the extra computational requirements of the first search,
# the initial tree construction is performed in parallel. Each
# child of the root spawns a new process, which is effective 
# because of the depth first nature of the search tree.
# --------------------------------------------------------------- 

from color import WHITE 
from nodes import InfinityNode
from position import Position
from minimax import search_position
from valuation import CONSTANTS

class SearchTree:

	def __init__(self, board, searchDepth=3):
		self.root = Position(board) 
		self.root.evaluate()
		self.searchDepth = searchDepth
		self.cutoffs = 0
		self.leavesSearched = 0


	def get_max_depth(self):
		return self.root.depth + self.searchDepth
 	
	def update_with_move(self, move):
		if self.root.children is None:
			self.root.create_children()
		for child in self.root.children:
			lastMove = child.lastMove
			sameStart = move.piece.square == lastMove.piece.square
			sameDest = move.endSquare == lastMove.endSquare
			if sameStart and sameDest:
				self.update_root(child)
				return self.root.board
		assert False

	def get_best_move(self):
		# initial search values (alpha: -inf, beta: inf)
		maximizeRoot = self.root.board.colorToMove == WHITE
		alpha = InfinityNode(isNegative=True) # -inf
		beta = InfinityNode(isNegative=False) # inf
		maxDepth = self.get_max_depth()

		# call the minimax function 
		optimalLeaf = search_position(self.root, alpha, beta, maximizeRoot, maxDepth)
		
		# assert optimalLeaf.board.colorToMove == WHITE
		# The optimal leaf is a decendant of the position created by the
		# best move. To get optimal position, iterate backwards through tree
		optimalPosition = optimalLeaf.get_ancestor(self.root.depth+1)
		print('leaf color: ' + str(optimalLeaf.board.colorToMove))
		# before returning the board of the optimal position, update
		# root allowing for subsequent calls to get next best position
		self.update_root(optimalPosition)
		return optimalPosition.lastMove, optimalPosition.board

	def update_root(self, position):
		self.root = position
		self.root.lastPosition = None

	# def printValueTemps(self):
	# 	bleh = ['Material','PST','Center Control','Connectivity','Mobility','Bishop Pair Bonus', 'Pawn Structure', 'Development','Pressure']

	# 	printStr = 'valuation: ' + str(self.root.valuation) + '\n'
	# 	for v,c,b in zip(self.root.valueTemps, CONSTANTS, bleh):
	# 		score = v*c
	# 		# printStr += f'\t{b}: {score}\n'
	# 		printStr += '\t' + str(b) + ': ' + str(score) + '\n'
	# 	print(printStr)
