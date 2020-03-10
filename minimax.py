# minimax.py
# --------------------------------------------------------------
# This file contains the search algorithm used to find optimal
# positions. It uses a minimax search with alpha-beta pruning 
# which has a time complexity of O(b^d), where b is the number 
# of legal moves and d is the maximum search depth. A minimax
# search minimizes loss by finding the optimal worst possible 
# outcome. It is a depth first search that eliminates branches 
# if a player's optimal worst position is worse than the openents 
# optimal worst ouotcome. This is possible because chess is a 
# zero sum game.
# --------------------------------------------------------------
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
# https://en.wikipedia.org/wiki/Minimax
# --------------------------------------------------------------

from nodes import InfinityNode

# Returns the leaf node of the optimal branch
def search_position(*args):
	position, alpha, beta, maximize, maxDepth = args
	# recursive base case: max depth reached
	if position.depth >= maxDepth+3:
		return position
	if position.depth >= maxDepth + 2 and not position.lastMove.isACapture:
		# position.evaluate()
		return position

	if position.children is None:
		position.create_children()
		position.children.sort(key=lambda c: c.valuation, reverse = maximize)

	if position.depth == maxDepth-3:
		children = position.children
	elif position.depth >= maxDepth:
		children = position.children[:5]
	else:
		children = position.children[:7]


	assert position.valuation is not None

	# make bestPosition the first child just to give it a starting value
	# It will be compared to its siblings and updated accordingly
	bestPosition = InfinityNode(isNegative=maximize)
	# bestPosition = None
	for child in children:
		assert child.depth-1 == position.depth
		# recursively call minimax on the child before comparing
		# it to its siblings to perform depth first search
		searchArgs = (child, alpha, beta, not maximize, maxDepth)
		positionNode = search_position(*searchArgs)
		assert positionNode is not None
		# compare positionNode to search values. If maximizing player,
		# maximize bestValue and alpha. If minimizing player, minimize
		# bestPosition and beta.
		# searchValues = (positionNode, bestPosition, alpha, beta, maximize)
		# bestPosition, alpha, beta = update_search_values(*searchValues)
		if maximize:
			bestPosition = max(positionNode, bestPosition)
			alpha = max(alpha, bestPosition)
		else:
			bestPosition = min(positionNode, bestPosition)
			beta = min(beta,bestPosition)

		# check for alpha-beta cutoff. If alpha is greater than beta, 
		# the opponents optimal worst outcome is better than own optimal
		# worst outcome. The branch is guaranteed to be suboptimal and 
		# should not be searched any deeper.
		if beta<=alpha: 
			break
	assert bestPosition is not None
	# store best child to avoid repeated search in later calls
	position.optimalChild = bestPosition
	return bestPosition
