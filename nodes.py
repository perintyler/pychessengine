# nodes.py
# --------------------------------------------------------------
# This file contains 3 types of nodes: InfinityNode, ComparableNode
# and PositionalNode. InfinityNode is the only class that gets
# instantiated directly (used to create min and max nodes).
# ComparableNode and PositionalNode are both abstract classes 
# that are inherited by the Position class (see position.py),
# which is used to create the search/decision tree (see tree.py) 
# responsible for find optimal moves. The comparable node class
# provides the functionality to compare nodes. The positional
# node class provides evaluation and parent functionality. A
# node's children and valuation, which are accessible through 
# property functions are not set on instantiation, since finding 
# moves and evaluating positions can be a relatively computationally
# expensive. They are only computed when the property is first
# accessed. This way, wasteful move generation and evaluation 
# on suboptimal branches is avoided.
# --------------------------------------------------------------

class ComparableNode:

	# implemented by position subclasses
	def get_comparison_value(self):
		pass

	def __lt__(self, other):
		return self.get_comparison_value() < other.get_comparison_value()
	
	def __le__(self, other):
		return self.get_comparison_value() <= other.get_comparison_value()

	def __gt__(self, other):
		return self.get_comparison_value() > other.get_comparison_value()

	def __ge__(self, other):
		return self.get_comparison_value() >= other.get_comparison_value()


class InfinityNode(ComparableNode):

	def __init__(self, isNegative=False):
		self.value = float('-inf') if isNegative else float('inf')

	def get_comparison_value(self):
		return self.value 


	def get_ancestor(self,depth):
		assert self.depth != depth
		ancestor = self.parent
		while ancestor.depth!=depth:
			ancestor = ancestor.parent
		return ancestor

