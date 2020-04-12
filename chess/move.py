# -*- coding: utf-8 -*-
"""Move Generation

Todo:
	- dont use json. use something with int keys
	- https://www.chessprogramming.org/Magic_Bitboards

put file loading into its own class
"""

from collections import namedtuple
from chess import PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING,WHITE,BLACK
from chess.bitboard import reverse as reverse_bitboard
from chess import board
from debug_tools import *

from pregame.data import MOVES, MOVE_SETS, MOVE_MASKS


# (MOVES,
#  MOVE_SETS,
#  RANK_MASKS,
#  FILE_MASKS,
#  DIAGONAL_MASKS,
#  ANTI_DIAGONAL_MASKS,
#  PAWN_BLOCKER_MASKS) = load_move_data_file()

# (RANK_MASKS,FILE_MASKS,DIAGONAL_MASKS,
#  ANTI_DIAGONAL_MASKS, PAWN_BLOCKER_MASKS) = MOVE_MASKS

Move = namedtuple('Move', 'startSquare endSquare isACapture')

class Generator:
	"""
	TODO: sliding piece mask needs to be applied in get moves
	"""
	def __init__(self, state):
		self.find_attacks(state)

		self.moves = []

		self.numMoves = 0
		self.numDefences = [0,0]
		self.numCenterAttacks = [0,0]


	def find_attacks(self, state):
		"""Finds and stores an attack set for each piece

		Change this to only take pieces and occupied parameter

		combined attack sets should get generated here

		count num center attacks

		count num defences
		"""
		self.attacks = ([],[])
		self.attackSets = [0,0]
		for piece,pieceType,color in state.get_pieces():
			# Pawn, King, Knight:
			# Retrieve precomputed, hashed attack set
			if pieceType == PAWN:
				pieceAttacks = MOVE_SETS[pieceType][color][piece][1]
			elif pieceType == KING or pieceType == KNIGHT:
				pieceAttacks = MOVE_SETS[pieceType][piece]

			# Bishop, Rook, Queen (sliding pieces):
			# compute attack set using blocker subtraction (o^())
			elif pieceType == ROOK:
				pieceAttacks = self.get_straight_move_set(piece, state.occupied)
			elif pieceType == BISHOP:
				pieceAttacks = self.get_diagonal_move_set(piece, state.occupied)
			elif pieceType == QUEEN:
				straightRays = self.get_straight_move_set(piece, state.occupied)
				diagonalRays = self.get_diagonal_move_set(piece, state.occupied)
				pieceAttacks = straightRays | diagonalRays
			self.attackSets[color] |= pieceAttacks
			self.attacks[color].append(pieceAttacks)

	def find_moves(self, state):
		color = state.colorToMove

		threatened = self.attackSets[not state.colorToMove]

		ownOccupation = state.colors[state.colorToMove]
		enemyOccupation = state.colors[not state.colorToMove]
		index = 0
		for piece, pieceType in state.pieces(state.colorToMove):
			pieceAttacks = self.attacks[color][index]
			index+=1

			# define moves and legal move mask depending on piece type
			if pieceType == PAWN:

				moveSet,attackSet = MOVE_SETS[PAWN][color][piece]
				blocker = MOVE_MASKS.pawnBlocker[color][piece]
				pawnIsBlocked = blocker & state.occupied == 0
				attackMask = attackSet & enemyOccupation
				moveMask = moveSet if pawnIsBlocked else 0
				legalMoveMask = attackMask | moveMask

			elif pieceType == KING:
				legalMoveMask = pieceAttacks & ~ownOccupation & ~threatened
			else:
				legalMoveMask = pieceAttacks & ~ownOccupation

			if pieceType == PAWN:
				moves = MOVES[PAWN][color][piece]
			else:
				moves = MOVES[pieceType][piece]

			for moveBitboard in moves:
				if moveBitboard & legalMoveMask != 0:
					'''remove isACapture from this file i think'''
					isACapture = moveBitboard & enemyOccupation != 0
					self.numMoves += 1
					move = Move(piece, moveBitboard, isACapture)
					self.moves.append(move)
					yield move

	def get_straight_move_set(self, piece, occupied):
		"""Rook/Queen Move gen"""
		# generate horizontal rays
		rankMask = MOVE_MASKS.rank[piece]
		rankMoves = self.subtract_blockers(piece, occupied, rankMask)

		# generate vertical rays
		fileMask = MOVE_MASKS.file[piece]
		fileMoves = self.subtract_blockers(piece, occupied, fileMask)

		# combine horizontal and vertical rays
		return rankMoves | fileMoves

	def get_diagonal_move_set(self, piece, occupied):
		"""Bishop/Queen Move gen"""
		# generate diagonal rays
		diagonalMask = MOVE_MASKS.diagonal[piece]
		diagonalMoves = self.subtract_blockers(piece, occupied, diagonalMask)

		# generate antidiagonal rays
		antiDiagonalMask = MOVE_MASKS.antidiagonal[piece]
		antiDiagonalMoves = self.subtract_blockers(piece, occupied,
												   antiDiagonalMask)

		# combine diagonal and antidiagonal rays into one bitset and return
		return diagonalMoves | antiDiagonalMoves

	def subtract_blockers(self, slider, occupied, mask):
		"""Sliding piece move generation by calculation

		https://www.chessprogramming.org/Subtracting_a_Rook_from_a_Blocking_Piece
		"""
		# calculate positive rays
		potentialBlockers = occupied & mask
		positiveRay = occupied ^ (potentialBlockers - (slider*2)) # o-2s
		positiveRay = positiveRay & mask


		# reverse the Bitboards, then get negative rays
		occupiedReversed = reverse_bitboard(occupied)
		maskReversed = reverse_bitboard(mask)
		sliderReversed = reverse_bitboard(slider)

		potentialBlockers = occupiedReversed & maskReversed
		negativeRay = occupiedReversed ^ (potentialBlockers - (sliderReversed*2))
		negativeRay = reverse_bitboard(negativeRay & maskReversed)

		# combine positive and negative rays into one Bitboard
		return positiveRay | negativeRay


class PriorityQueue:
	"""Todo
		- recapture with least valuable piece
		- https://www.chessprogramming.org/MVV-LVA
		- should this be here or in search?

	Priorities:
		1: PV Node
		2: good captures
		3: killer moves (same depth or -2 depth)
	"""
	def __init__(self): pass

	# def get_attacks_for_piece(self, pieceType, piece, occupied, color):
	# 	if pieceType == PAWN:
	# 		return ATTACK_SETS[pieceType][color][piece]
	#
	# 	elif pieceType == ROOK:
	# 		return self.get_straight_move_set(piece, occupied)
	#
	# 	elif pieceType == BISHOP:
	# 		return self.get_diagonal_move_set(piece, occupied)
	#
	# 	elif pieceType == QUEEN:
	# 		straightRays = self.get_straight_move_set(piece, occupied)
	# 		diagonalRays = self.get_diagonal_move_set(piece, occupied)
	# 		return straightRays | diagonalRays
	#
	# 	elif pieceType == KING or pieceType == KNIGHT:
	# 		return ATTACK_SETS[pieceType][piece]
	#
	# def get_moves_for_piece(self, piece, pieceType, color, occupation, attacks):
	# 	ownOccupation,enemyOccupation = occupation
	# 	ownAttacks, threatened = attacks
	# 	if pieceType == PAWN:
	# 		# captures, moves = pseudoLegalMoves
	# 		attackMask = ownAttacks & enemyOccupation
	# 		blocker = PAWN_BLOCKER_MASKS[color][piece]
	# 		moveMask = blocker & ~(ownOccupation | enemyOccupation)
	#
	# 		legalMoveMask = attackMask | moveMask
	# 		captures = MOVES[pieceType][color][piece][0]
	# 		nonCaptures = MOVES[pieceType][color][piece][1]
	# 		moves = captures + nonCaptures
	# 	elif pieceType == KING:
	# 		legalMoveMask = ~ownOccupation & ~threatened
	# 		moves = MOVES[pieceType][piece]
	#
	# 	else:
	# 		legalMoveMask = ~ownOccupation
	# 		moves = MOVES[pieceType][piece]
	#
	# 	for moveBitboard in moves:
	# 		if moveBitboard & legalMoveMask != 0:
	# 			isACapture = moveBitboard & enemyOccupation != 0
	# 			yield Move(piece, moveBitboard, isACapture)

	# def generate_sliding_piece_moves(self, slider, occupied, mask):
	# 	"""Queen, Rook, and Bishop Move Validation
	#
	# 	:param slider:
	# 	:param occupied:
	# 	:param mask:
	#
	# 	"""
	#
	# 	positiveRay = self._subtract_blockers(slider,occupied,mask)
	#
	# 	def reverse_bits(bitboard):
	# 		reversedBits  = 0
	# 		for _ in range(64):
	# 			reversedBits <<= 1
	# 			reversedBits |= bitboard & 1
	# 			bitboard >>= 1
	# 		return reversedBits
	#
	# 	revSlider,revOccupied,revMask = (reverse_bits(slider),
	# 									 reverse_bits(occupied),
	# 									 reverse_bits(mask))
	#
	# 	# to generate negative rays, you need to reverse the bitboards
	# 	negativeRay = self._subtract_blockers(revSlider,revOccupied,revMask)
	# 	negativeRay = reverse_bits(negativeRay)
	# 	return positiveRay | negativeRay
	#
	# def _subtract_blockers(self, slider, occupied, mask):
	# 	"""o^(o-2r)"""
	# 	potentialBlockers = occupied & mask
	# 	ray = occupied ^ (potentialBlockers - (slider*2)) # o-2s
	# 	return ray & mask

#
# # sliding piece move generation by calculation: o^(o-2s)
# def subtract_blockers(self, slider, occupied, mask):
#
#     # calculate positive rays
#     potentialBlockers = occupied & mask
#     positiveRay = occupied ^ (potentialBlockers - (slider*2)) # o-2s
#     positiveRay = positiveRay & mask
#
#     # reverse the Bitboards, then get negative rays
#     occupiedReversed = board.reverse_bits(occupied)
#     maskReversed = board.reverse_bits(mask)
#     sliderReversed = board.reverse_bits(slider)
#
#     potentialBlockers = occupiedReversed & maskReversed
#     negativeRay = occupiedReversed ^ (potentialBlockers - (sliderReversed*2))
#     negativeRay = board.reverse_bits(negativeRay & maskReversed)
#
#     # combine positive and negative rays into one Bitboard
#     return positiveRay | negativeRay
#
#
# def get_attacks_for_piece(self, pieceType, pieceBitboard, boardOccupation, color):
#     pieceSquare = board.SQUARE_LOOKUP[pieceBitboard]
#     if pieceType == PAWN:
#         # attacks,moves = MOVES[pieceType][color][pieceSquare]
#         attacks = ATTACK_SETS[pieceType][color][pieceSquare]
#         pawnIsBlocked = not (upOne & boardOccupation).is_empty()
#         pawnIsBlocked = chess.PAWN_BLOCKER_MASKS[pieceSquare] & boardOccupation != 0
#         if pawnIsBlocked:
#             moves = chess.board.bitboard.EMPTY
#
#         return attacks #, moves
#     elif pieceType == ROOK:
#         return get_straight_rays(pieceBitboard, boardOccupation)
#     elif pieceType == BISHOP:
#         return get_diagonal_rays(pieceBitboard, boardOccupation)
#     elif pieceType == QUEEN:
#         straightRays = get_straight_move_set(pieceBitboard, boardOccupation)
#         diagonalRays = get_diagonal_move_set(pieceBitboard, boardOccupation)
#         return straightRays | diagonalRays
#     elif pieceType == KNIGHT or pieceType == KING:
#         return ATTACK_SETS[pieceType][pieceSquare]
