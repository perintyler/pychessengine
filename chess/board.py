# -*- coding: utf-8 -*-
"""Board Representation

Todo:
	- state -> mutable list
	- backward move traversal
"""

from collections import namedtuple

from pregame.data import (INITIAL_PIECES, NUM_PIECES, COLOR_RANGES,
						  PIECE_TYPE_LOOKUP, COLOR_LOOKUP)

from settings import PIECE_REPRESENTATION
from debug_tools import *

# from pregame.board import NUM_PIECES, PIECE_INDEX_LOOKUPS, PIECE_CHARS
class PieceSet(list):
	'''Stores pieces

	Pieces will always be stored in the same index for any given board state.
	When a piece is captured, its index will store an empty bitboard. This
	allows for fast piece type lookup and iteration.

	Iterate a specific piece type:
	>>> whitePieces = PieceSet(whitePieceBitboards)
	>>> for pawn in whitePieces(PAWN)

	TODO: make piece set inherit list not tuple and add update function to state
	'''

	# figure out if its better to have them here or globally
	# FULL_RANGE = (0,NUM_PIECES)
	'''make these static vars global'''
	UNICODES = (
		['♟', '♞', '♝','♜', '♛', '♚'],
		['♙', '♘', '♗', '♖', '♕', '♔']
	)

	TYPES = [PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING] = range(6)

	# make indexers a name tuple
	# move initial bitboards down below
	# (INITIAL_BITBOARDS,
	#  NUM_PIECES,
	#  FULL_RANGE,
	#  COLOR_RANGES,
	#  RANGE_LOOKUP,
	#  COLOR_LOOKUP,
	#  TYPE_LOOKUP) = load_board_data_file()

	# def __new__(cls, pieces):
	# 	return super().__new__(cls,pieces)
	#
	# def __init__(self, pieces):
	# 	self.iterIndex,self.iterStopIndex = PieceSet.FULL_RANGE

	def __init__(self, *args):
		list.__init__(self, *args)
		self.iterIndex = 0
		self.iterStopIndex = NUM_PIECES

	'''make sure this works
	this could actually return iter(self)
	'''
	def __call__(self, colorToIterate):
		'''Sets iteration type and returns itself'''
		self.iterIndex,self.iterStopIndex = COLOR_RANGES[colorToIterate]
		return self

	def __iter__(self): return self

	def __next__(self):
		while self.iterIndex != self.iterStopIndex:
			piece,pieceType,pieceColor = self[self.iterIndex]
			self.iterIndex += 1
			if piece == 0: continue
			return piece,pieceType

		# reset iteration values before stopping iteration
		self.iterIndex,self.iterStopIndex = 0,NUM_PIECES
		raise StopIteration


	def __getitem__(self, index):
		piece = super().__getitem__(index)
		pieceType = PIECE_TYPE_LOOKUP[index]
		pieceColor = COLOR_LOOKUP[index]
		return piece,pieceType,pieceColor

	# def get_color(self, color):
	# 	startIndex,endIndex = PieceSet.COLOR_RANGES[color]
	# 	for i in range(startIndex,endIndex):
	# 		piece,pieceType,pieceColor = self[i]
	# 		if piece==0: continue
	# 		yield piece,pieceType

	@property
	def bitboards(self):
		for piece in self:
			yield piece

	@property
	def all(self):
		for i in range(NUM_PIECES):
			yield self[i]

	# def get_king(self, color):
	# 	return self[PieceSet.INDEX_RANGES[color][KING][0]]
	#
	# def get_piece_type(self,pieceType):
	# 	'''Is this ever used???'''
	# 	for color in [WHITE,BLACK]:
	# 		start,end = PieceSet.RANGE_LOOKUP[color][pieceType]
	# 		for i in range(start,end):
	# 			piece  = self[i]
	# 			if piece == 0: continue
	# 			yield piece

	# def get_color_group(self, color):
	# 	'''If this is only used once in state init, get rid of this'''
	# 	startIndex,endIndex = PieceSet.COLOR_RANGES[color]
	# 	for index in range(startIndex,endIndex):
	# 		piece = self[index]
	# 		if piece == 0: continue
	# 		yield self[index]

CastlingRights = namedtuple('CastlingRights','kingside queenside')

class State:
	"""Board Positional State. inherit object and piece set"""

	"""TODO: update/pop"""
	def __init__(self, colorToMove, pieces):
		self.pieces = PieceSet(pieces)
		self.colorToMove = colorToMove

		# self.pieceTypes = [0 for _ in range(6)]
		self.colors = [0 for _ in range(2)]
		self.occupied = 0
		# create an occupation bitboard for each color to store piece locations
		for piece, pieceType, pieceColor in self.get_pieces():
			# self.pieceTypes[pieceType] |= piece
			self.colors[pieceColor] |= piece
			self.occupied |= piece

	def __add__(self, move):
		pass

	def __sub__(self, move):
		pass

	def get_pieces(self):
		for piece,pieceType,pieceColor in self.pieces.all:
			if piece == 0: continue
			yield piece,pieceType,pieceColor

	"""serialize makes no sense now that state inherits pieceset"""
	def serialize(self, move):
		"""Creates new tuples of piece bitboards that result from given move

		The pieces for the color that just moved will always be returned first,
		followed by the other color's pieces.
		"""
		serialized = []

		for piece,pieceType,color in self.pieces.all:
			if color == self.colorToMove and piece == move.startSquare:
				serialized.append(move.endSquare)
			elif color != self.colorToMove and move.isACapture:
				'''I can get capture index here with 0 bb check'''
				serialized.append(piece & ~move.endSquare)
			else:
				serialized.append(piece)

		return serialized

	# def __repr__(self):
	# 	return f'<State colorToMove={self.colorToMove} occupied={self.occupied}>'
	def __str__(self):
		squares = ['.']*64 # empty square represented as '.'
		for piece,pieceType,color in self.get_pieces():
			isBitOn = lambda index: piece & (1 << (63-index)) != 0
			square = list(map(isBitOn, range(64))).index(True)
			squares[square] = PIECE_REPRESENTATION[color][pieceType]
		formatRow = lambda rowIndex: ''.join(squares[rowIndex:rowIndex+8])
		return '\n'.join(map(formatRow, range(0,64,8)))


State.INITIAL = State(0, INITIAL_PIECES)


def parse_pgn(pgnStr): pass
