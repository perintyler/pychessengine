# position.py
# --------------------------------------------------------------
# This file contains the Position class. Position objects serve as
# the nodes that make up the search tree in tree.py. It stores
# a board, the last move, and since it inherits PositionalNode, 
# it has access to its parent, allowing for backwards traversal 
# through the search tree. It also inherits comparison functionality
# from ComparableNode. Comparisons are determined by the boards 
# valuation. When it is first instantiated, it will not have children.
# Creating children requires finding moves, but since the search
# tree state is mantained, the children only need to created once.
# --------------------------------------------------------------	

from nodes import ComparableNode
from move_generation import find_moves,CastleMove
from valuation import valuator
from color import WHITE


class Position(ComparableNode):

	def __init__(self, board, lastPosition=None, lastMove=None):
		self.depth = 0 if lastPosition is None else lastPosition.depth+1
		self.lastPosition = lastPosition
		self.lastMove = lastMove
		self.board = board
		self.optimalChild = None
		self.numMoves = 0
		self.valuation = None
		self.children = None

		self.valueTemps = None

	
	def evaluate(self):
		# self._valuation = valuator(self)
		self.valuation = valuator(self)

	def get_comparison_value(self):
		assert self.valuation is not None
		return self.valuation

	def last_move_was_capture(self):
		return self.lastMove.isACapture

	
	def create_children(self):
		legalMoves = find_moves(self.board)
		self.children = list(map(self.create_child, legalMoves))
		
	def create_child(self, move):
		self.numMoves+=1
		updatedBoard = self.board.make_move(move)
		p = Position(updatedBoard, lastPosition=self, lastMove=move)	
		p.evaluate()
		return p

	def __str__(self, level=0):
		ret = '\t'*level+str(self.valuation)+'\n'
		if self.children is not None:
			for child in self.children:
				ret += child.__str__(level+1)
		return ret


	def get_ancestor(self,depth):
		assert self.depth != depth
		ancestor = self.lastPosition
		while ancestor.depth!=depth:
			ancestor = ancestor.lastPosition
		return ancestor

