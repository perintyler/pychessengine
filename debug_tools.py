"""Debuging Developer Tools

Utilities Included:
	- Search Moniter
	- method timing and profiling
	- debug print functions
		+ bitboard
		+ piece properties
		+ state properties
		+ move generator properties

TODO:
	- clean this file up
"""

import time
import os

def save_game(allMoves):
	pass

def delete_data_files():
	if input('are you sure you want to delete all data files? (y/n)') != 'y':
		print('cancelling data file deletion')
	else:
		from settings import DATA_DIRECTORY
		for fileName in os.listdir(DATA_DIRECTORY):
			if fileName.endswith('.json'):
				print(f'deleting data file \'{fileName}\'')
				dataFilePath = os.path.join(DATA_DIRECTORY, fileName)
				os.remove(dataFilePath)

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
		self.depths = [0]*10

	def alpha_cutoff(self):
		self.alphaCutoffs += 1

	def beta_cutoff(self):
		self.betaCutoffs+=1

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

class TreeStringBuilder:
	"""TODO: Implement"""

	def __init__(self):
		self.str = ''

	def add_node(self, value, level):
		self.str += '\t'*level+str(value)+'\n'

	def print_results(self):
		print(self.str)


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

def get_square_notation(square):
	x = 7-(square % 8)
	y = (square // 8)
	rankStr = 'abcdefgh'[x]
	fileStr = str(y+1)
	return rankStr + fileStr


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
		print(f'{colorStr} {typeStr} has been captured')
	else:
		notatedSquare = get_square_notation(square)
		print(f'{colorStr} {typeStr} on {notatedSquare}')


def print_move(move):
	startLoc = get_piece_location(move.startSquare)
	endLoc = get_piece_location(move.endSquare)
	print(f'<Move from={startLoc} to={endLoc} capture={move.isACapture}>')

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
