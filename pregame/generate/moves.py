# -*- coding: utf-8 -*-
"""Pre-Game Bitboard Generation

Move Bitboard Generation
Attack Bitboard Generation
Board Masks generation

TODO:
	- make diagonal masks
"""
import os
import json

from chess.bitboard import create as create_bitboard
from pregame.utils import get_coordinate,get_square


# TODO import these
WHITE,BLACK = 0,1
PIECE_TYPES = [PAWN,KNIGHT,BISHOP,ROOK,QUEEN,KING] = range(6)
SQUARES = list(range(64))

#################################################################
# DIRECTION UTILS                         						#
#################################################################

def N(x,y,d=1): return x,y+d
def E(x,y,d=1): return x+d,y
def S(x,y,d=1): return x,y-d
def W(x,y,d=1): return x-d,y
def NE(x,y,d=1): return x+d,y+d
def SE(x,y,d=1): return x+d,y-d
def SW(x,y,d=1): return x-d,y-d
def NW(x,y,d=1): return x-d,y+d

STRAIGHT_DIRECTIONS = [N,E,S,W]
DIAGONAL_DIRECTIONS = [NE,SE,SW,NW]
ALL_DIRECTIONS = [N,NE,E,SE,S,SW,W,NW]

def get_rays(x,y, directions, numSteps=8):
	makeNSteps = lambda n: [d(x,y,n) for d in directions]
	return sum(map(makeNSteps, range(1,numSteps)),[])



#################################################################
# MOVE BITBOARD GENERATION (KNIGHT,BISHOP,ROOK,QUEEN,KING)      #
#################################################################

def get_moves(pieceType, square, color=None):
	x,y = get_coordinate(square)

	def get_valid_squares(moves):
		"""returns end squares for moves on the board"""
		return [get_square(*m) for m in moves if 0<=m[0]<8 and 0<=m[1]<8]

	def get_pawn_moves():
		assert color is not None
		# Pawn is the only piece type whos moves depend on its color. white pawns
		# move in the positive y direction, and black in the negative y direction
		# pawns can move one step forward. If the pawn is on its starting square
		# it can move two steps forward. Pawns can capture diagonally forward
		direction = 1 if color == WHITE else -1
		oneStepMove,twoStepMove = (x,y+direction),(x, y+2*direction)
		captureLeft,captureRight = (x-1, y+direction),(x+1, y+direction)

		pawnIsOnStartRank = color==WHITE and y==1 or color==BLACK and y==6
		moves = [oneStepMove,twoStepMove] if pawnIsOnStartRank else [oneStepMove]
		attacks = [captureLeft,captureRight]

		return get_valid_squares(moves), get_valid_squares(attacks)

	def get_knight_moves():
		moves = []
		for d1 in [N,S]:
			for d2 in [W,E]:
				moves.append(d1(*d2(x,y),2)) # 2 steps in d1, 1 step in d2
				moves.append(d2(*d1(x,y),2)) # 2 steps in d2, 1 step in d1
		return get_valid_squares(moves)

	def get_sliding_moves():
		"""Bishop,Rook,Queen,King"""
		moves = get_rays(x,y, {
			BISHOP: DIAGONAL_DIRECTIONS,
			ROOK:	STRAIGHT_DIRECTIONS,
			QUEEN:	ALL_DIRECTIONS,
			KING:	ALL_DIRECTIONS
		}[pieceType], numSteps = 1 if pieceType == KING else 8)
		return get_valid_squares(moves)

	if pieceType == PAWN:
		return get_pawn_moves()

	elif pieceType == KNIGHT:
		return get_knight_moves()
	else:
		return get_sliding_moves()


def generate_move_data():

	def create_bitboards_for_piece_type(pieceType):
		if pieceType == PAWN:
			moves = [{}, {}] # white Moves,black Moves
			moveSets = [{}, {}] # white move sets, black move Sets
			for color in [WHITE,BLACK]:
				for square in SQUARES:
					squareKey = create_bitboard([square])
					captures,nonCaptures = get_moves(pieceType, square, color)
					allMoves = captures+nonCaptures

					moveBitboards = [create_bitboard([m]) for m in allMoves]
					moves[color][squareKey] = moveBitboards

					captureMoveSet = create_bitboard(captures)
					nonCaptureMoveSet = create_bitboard(nonCaptures)
					moveSetsForSquare = (captureMoveSet,nonCaptureMoveSet)
					moveSets[color][squareKey] = moveSetsForSquare

			return moves,moveSets
		else:
			moves = {}
			moveSets = {}
			for square in SQUARES:
				squareKey = create_bitboard([square])

				allMoves = get_moves(pieceType, square)
				moves[squareKey] = [create_bitboard([m]) for m in allMoves]
				moveSets[squareKey] = create_bitboard(allMoves)
			return moves,moveSets

	moves,moveSets = [],[]
	for pieceType in [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING]:
		bitboards = create_bitboards_for_piece_type(pieceType)
		movesForPiece,moveSetsForPiece = bitboards
		moves.append(movesForPiece)
		moveSets.append(moveSetsForPiece)

	return {'moves': moves, 'move sets': moveSets}



#
# def save_move_bitboards_to_file():
# 	"""This is what is called outside this file"""
# 	movesFileName = 'moves.json'
# 	movesFilepath = os.path.join(DATA_DIR, movesFileName)
# 	if os.path.exists(movesFilepath):
# 		prompt = 'move file already generated. delete file and regenerate? (y/n)'
# 		if input(prompt) == 'y':
# 			os.remove(movesFilepath)
# 		else:
# 			print('exiting move bitboard generation')
# 			return
#
#
# 	# save bitboards to file
# 	with open(movesFilepath, 'w') as movesFile:
# 		json.dump(generate_move_data(), movesFile)
