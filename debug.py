# -*- coding: utf-8 -*-
"""Assortment of tools only intended for development and debugging"""

import time
import sys, os
import re

COLOR_LABELS = ['white','black']
PIECE_LABELS = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
EVALUATION_LABELS = [
		  'Material', 'Piece Square Table', 'Development', 'Center Control', 'Connectivty',
		  'Mobility', 'Bishop Pair Bonus', 'Pawn Structure', 'Development',
		  'Pressure', 'Connected Rooks', 'King Safety', 'Outposts'
]
EVALUATION_MODE_LABELS = ['Lazy','Default','Eager']

methods = set()
runtimes = {}

def clear_terminal():
	os.system('cls' if os.name == 'nt' else 'clear')

def log(moves):
	pass


def wipe_data():
	if input('are you sure you want to delete all data files? (y/n)') != 'y':
		print('cancelling data file deletion')
	else:
		from settings import DATA_DIRECTORY
		for fileName in os.listdir(DATA_DIRECTORY):
			if fileName.endswith('.json'):
				print(f'deleting data file \'{fileName}\'')
				dataFilePath = os.path.join(DATA_DIRECTORY, fileName)
				os.remove(dataFilePath)


def print_evaluator(e):
	from chess.evaluate  import WEIGHTS
	print('Evalutor Debug')
	print(f'\tmode: {EVALUATION_MODE_LABELS[e.mode]}')
	print('\t' + ' '*30 + 'white\tblack\tdif\tweighted')


	for whiteScore,blackScore,label,weight in zip(e.scores[0],e.scores[1], EVALUATION_LABELS, WEIGHTS):
		spacing = ' '*(30-len(label))
		dif = whiteScore-blackScore
		weighted = round(weight*dif, 3)
		propertyStr = f'{whiteScore}\t{blackScore}\t{dif}\t{weighted}'
		print(f'\t{label}:{spacing}{propertyStr}')

def get_test_results():
	import unittest
	# disable print
	sys.stdout = open(os.devnull, 'w')
	# run tests
	result = unittest.main(module='chess', exit=False).result
	# re enable print
	sys.stdout = sys.__stdout__


	# parse test results and return as formatted result str
	testsPassed = not result.failures and not result.errors
	if testsPassed:
		return 'success'
	else:
		resultStr = ''
		def parse_results(results, title):
			methodNames = ' '.join([f[0]._testMethodName for f in results])
			traces = '\n'.join([f[1] for f in results])
			resultStr += f'{title}: {methodNames}\n{title} traces:\n{traces}\n'

		if result.failures: parse_results(result.failures, 'Failure')
		if result.errors: parse_results(result.errors, 'errors')

		return resultStr


class Square:

	def __init__(self, index):
		self.index = index

	@property
	def notation(self):
		x = (self.index % 8)
		y = 8-(self.index // 8)
		rankStr = 'abcdefgh'[x]
		fileStr = str(y)
		return rankStr + fileStr


class Bitstring(str):

	def __new__(cls, bitboard):
		binStr = bin(bitboard)[2:]
		numMissingBits = 64 - len(binStr)
		bitboardStr = '0'*numMissingBits + binStr
		return str.__new__(cls, bitboardStr)


	def count_bits(self): return self.count('1')

	def is_on(self, bit): return self[bit] == '1'

	def get_row(self, rowNum): return self[rowNum*8:rowNum*8+8]

	def format(self):
		formatted = '\n'.join(map(self.get_row, range(8)))
		if self.count_bits() == 1 or self.count_bits() == 0:
			formatted = re.sub('1','X', re.sub('0','.',formatted))
		return formatted

	def print(self, title):
		header = '*' + title + '*'
		print(header + '\n' + self.format())

	@staticmethod
	def print_all(*elements, indent='', titles=None):
		spacing = ' '*8 + '\t'


		bitstrings = [Bitstring(e) if type(e) is int else e for e in elements]
		if titles:
			print(indent + spacing.join(titles))

		for r in range(8):
			rows = [bs.format().split('\n')[r] for bs in bitstrings]
			print(indent + '\t'.join(rows))



	@property
	def square(self):
		assert self.count_bits() == 1
		return Square(self.index('1'))


class Piece:

	def __init__(self, value, ptype, color):
		self.value,self.ptype,self.color = value, ptype, color

	def __str__(self):
		typeStr = get_piece_type_str(self.ptype)
		colorStr = get_color_str(self.color)

		square = get_piece_location(self.value)
		if square == -1:
			return f'captured {colorStr} {typeStr}'
		else:
			return f'{colorStr} {typeStr} on {Square(square).notation}'

class SearchDebugger:

	def __init__(self, root, evaluator, generator):
		self.root = root
		self.evaluator = evaluator
		self.generator = generator

	def debug(self):
		pass

class Debugger:

	PRINT_MOVES = True


	def __init__(self, state, e, g):
		self.state = state
		self.e,self.g=e,g
		# self.debug_moves()
		self.debug_evaluate()

	def debug_moves(self):


		if self.g:
			g=self.g
		else:
			from chess.moves import Generator
			g = Generator()
			g.find_attacks(self.state)
			g.find_moves(self.state)

		# moves = list(g.find_moves(self.state))

		colorLabel = COLOR_LABELS[self.state.colorToMove]
		print('Moves Debug')
		print(f'\tNum Moves for {colorLabel}: {len(g.moves)}\n')
		print('\tAttack Sets')
		Bitstring.print_all(*g.attackSets,indent='\t\t',titles=['white','black'])
		if Debugger.PRINT_MOVES:
			print('\tMoves:')
			for piece,pieceType,color in self.state.pieces:
				moveStrs = []
				while not g.moves.is_empty():
					move = g.moves.pop()
					if move.startSquare == piece:
						s2 = Bitstring(move.endSquare).square
						symbol = 'x' if move.captureType is not None else ''
						moveStrs.append(f'{symbol}{s2.notation}')
				if len(moveStrs) == 0: continue
				pieceStr = f'{PIECE_LABELS[pieceType]} on {Bitstring(piece).square.notation}'
				moveListStr = ', '.join(moveStrs)
				print(f'\t\t{pieceStr}:\t{moveListStr}' )
		print()
		self.g = g
		return self

	def debug_evaluate(self):

		if self.e:
			e=self.e
		else:
			from chess.evaluate import Evaluator,WEIGHTS
			e = Evaluator()
			e(self.state, self.g.attacks) #, self.g.moves, self.g.attacks)

		print('Evalutor Debug')
		print(f'\tmode: {EVALUATION_MODE_LABELS[e.mode]}')
		print('\tValuation: ' + str(e.valuation))
		print('\t' + ' '*30 + 'white\tblack\tdif\tweighted')


		for whiteScore,blackScore,label,weight in zip(e.scores[0],e.scores[1], EVALUATION_LABELS, e.weights):
			spacing = ' '*(30-len(label))
			dif = whiteScore-blackScore
			weighted = round(weight*dif, 3)
			propertyStr = f'{whiteScore}\t{blackScore}\t{dif}\t{weighted}'
			print(f'\t{label}:{spacing}{propertyStr}')

		return self



#################################################################
# SEARCH DEBUG UTILS                         					#
#################################################################


class SearchMonitor:

	def __init__(self):
		self.reset()

	def reset(self):
		self.alphaCutoffs = 0
		self.betaCutoffs = 0
		self.nodesSearched = 0
		self.depths = [0]*50

	def cutoff(self, maximize):
		if maximize:
			self.alphaCutoffs += 1
		else:
			self.betaCutoffs += 1

	def node_searched(self,depth):
		self.nodesSearched += 1
		self.depths[depth]+=1

	def print_results(self):
		self.depths.append(0)
		print(f'{self.nodesSearched} nodes searched')
		print(f'There were {self.alphaCutoffs} alpha cutoffs and {self.betaCutoffs} beta cutoffs')
		for i,numSearched in enumerate(self.depths):
			if numSearched==0: continue
			print(f'{numSearched} nodes searched at depth {i}')

#################################################################
# TIME DEBUG UTILS                         						#
#################################################################

class MethodProfile:

	def __init__(self,name):
		self.name = name
		self.timesRun = self.timeSpent = 0

	def addTime(self,time):
		self.timesRun += 1
		self.timeSpent += time

	def __str__(self):
		if self.timesRun == 0: return 'never ran ' + self.name
		averageRuntime = self.timeSpent / self.timesRun
		return '' + self.name + '\t\t' + str(self.timesRun) + '\t\t' + str(averageRuntime)
		# return f'{self.name}\t\t\t{self.timesRun}\t\t{averageRuntime}

methodProfiles = set()

# operator to time methods
def timeit(method):
	profile = MethodProfile(method.__name__)
	methodProfiles.add(profile)

	def timed(*args, **kw):
		# store time before method is called
		methodStartTime = time.time()
		result = method(*args, **kw)

		# add
		profile.addTime(methodEndTime - methodStartTime)
		return result


	return timed

def print_execution_times():
	for m in methodProfiles:
		print(m)


#################################################################
# PRINT DEBUG UTILS                         					#
#################################################################




def print_bitboard(bitboard, title=None):
	binStr = bin(bitboard)[2:] 		# strip leading 0b
	binStr = '0'*(64 - len(binStr)) + binStr # make 64 bits by adding leading 0 padding
	rows = map(lambda i: binStr[i:i+8], range(0,64,8))
	bitboardStr = '\n'.join(rows)
	titleStr = '' if title is None else '*' + title + '*'
	print('\n'.join([titleStr, bitboardStr]))


class Node:

	def __init__(self, val, depth):
		self.val = val
		self.depth = depth
		self.children = []
		self.best = False
		self.maximizing = None
		self.display = None

	def __str__(self):
		indent = '\t'*self.depth
		if self.depth != 3:
			valStr = self.display
		else:
			valStr = str(self.val)

		if self.best:
			valStr = f'({valStr})'
		if self.maximizing is not None:
			valStr += '-B' if self.maximizing else '-s'
		return indent + valStr
		# return '\t'*self.depth + self.val if not self.best else f'({self.val})'

class TreeBuilder:
	"""TODO: Implement"""

	def __init__(self):
		self.str = ''
		self.cache = {}
		self.root = None

	def set_root(self,rootVal,rootState):
		self.root = Node(rootVal, 0)
		self.cache['0'+str(rootState)] = self.root

	def add_node(self, val, depth, childState, parentState, maximizing=None):
		childHash = str(depth) + str(childState)
		parentHash = str(depth-1) + str(parentState)

		n = Node(val, depth)
		n.maximizing = maximizing
		self.cache[childHash] = n
		self.cache[parentHash].children.append(n)


	def set_best(self, state, val, depth):
		hash = str(depth) + str(state)
		p = self.cache[hash]
		p.display = str(val)
		for child in p.children:
			if child.val == val:
				child.best = True
				break

	def print(self):
		#self.traverse(self.root)
		self.traverse(self.root)

	def traverse(self,node):
		print(node)
		for child in node.children:
			self.traverse(child)

	def visualize_decisions(self):
		self.traverse_best(self.root)

	def traverse_best(self,node):
		best = None
		comp = ''
		for c in node.children:
			if c.best:
				best = c
			else:
				if c.display is None:
					comp += str(c.val) + ','
				else:
					comp += str(c.display) + ','
		if best is not None:
			cs = f'({best.val}) - {comp}'
			m = '-B' if not node.maximizing else '-s'
			print('\t'*node.depth + m + cs)
		for c in node.children:
			self.traverse_best(c)

def get_piece_type_str(pieceType):
	return {
		0: 'pawn',
		1: 'knight',
		2: 'bishop',
		3: 'roook',
		4: 'queen',
		5: 'king'
	}[pieceType]

def get_color_str(color):
	return {0: 'white', 1: 'black'}[color]



def get_piece_location(piece):
	for index in range(64):
		mask = 1 << (63-index)
		if mask & piece != 0:
			return index
	return -1

def print_piece(piece,pieceType,pieceColor):
	typeStr = get_piece_type_str(pieceType)
	colorStr = get_color_str(pieceColor)

	square = get_piece_location(piece)
	if square == -1:
		print(f'Cannot print {colorStr} {typeStr}. It was captured')
	else:
		notatedSquare = get_square_notation(square)
		print(f'{colorStr} {typeStr} on {notatedSquare}')


def print_move(m, detailed=False):
	if not detailed:
		m0 = Bitstring(m.start).square.notation
		m1 = Bitstring(m.end).square.notation
		symbol = 'x' if m.captureType is not None else '->'
		print(m0 + symbol + m1)
	# print(f'<Move from={startLoc} to={endLoc} capture={move.isACapture}>')

def debug_state(state):
	print('all pieces')
	print_bitboard(state.occupied)
	print('white occupancy')
	print_bitboard(state.colors[0])
	print('black occupancy')
	print_bitboard(state.colors[1])
	for pieceTypes,pieceOccupancy in enumerate(state.pieceTypes):
		print('occupancy for ' + get_piece_type_str(pieceTypes))
		print_bitboard(pieceOccupancy)

def debug_move_generator(generator):
	print('attacks found = ' + str(generator.attacks is not None))
	print('moves found = ' + str(generator.moves is not None))
	print('num legal moves = ' + str(generator.numMoves))
	if generator.moves is not None:
		for move in generator.moves:
			print_bitboard(move)
