# -*- coding: utf-8 -*-
"""Loads Stored Engine Data"""

import os

import json
import pickle
from collections import namedtuple

from chess.pregame.save import DATA_DIRECTORY, DATA_FILES

isDigit = lambda k: k.lstrip('-').isdigit()
parseJson = lambda d: {int(k) if isDigit(k) else k:v for k,v in d.items()}

def load_data_file(fileName):
	"""Loads json and pickle data files"""
	fileType = os.path.splitext(fileName)[1]
	fileMode = 'r' if fileType == '.json' else 'rb'
	path = os.path.join(DATA_DIRECTORY, fileName)
	with open(path, fileMode) as dataFile:
		load = pickle.load if fileType == '.pickle' else json.load
		fileContents = load(dataFile)
	return fileContents

def create_mask_set(maskSetName, maskTypes):
	MaskSet = namedtuple(maskSetName + 'Masks', maskTypes)
	masks = load_data_file(DATA_FILES.masks)
	return MaskSet(*[masks[mask] for mask in maskTypes])

def load_move_masks():
	maskTypes = ('ranks','files','diagonals','antidiagonals',
				 'reversedRanks','reversedFiles','reversedDiagonals',
				 'reversedAntidiagonals', 'reversedSquares', 'pawnBlockers')
	return create_mask_set('Move', maskTypes)

def load_move_cache():
	moveFileData = load_data_file(DATA_FILES.moves)
	return moveFileData['moves'], moveFileData['move sets']

def load_magic():
	magicData = load_data_file(DATA_FILES.magic)
	MagicCache = namedtuple('MagicCache', 'cache bitboards attacks indecies')
	return [MagicCache(*magicData[piece]) for piece in ['bishop', 'rook']]

def load_evaluation_masks():
	maskTypes = ('centerSquares', 'centerFiles', 'minorPieceSquares')
	return create_mask_set('Evaluation', maskTypes)

def load_piece_square_tables():
	return load_data_file(DATA_FILES.board)['pst']

def load_initial_pieces():
	return load_data_file(DATA_FILES.board)['initial pieces']

def load_piece_index_values():
	indexerTypes = ['num pieces', 'piece type lookup',
					 'piece color lookup', 'color ranges']
	indexers = load_data_file(DATA_FILES.board)['piece index values']
	return (indexers[label] for label in indexerTypes)

def load_hash_values():
	return load_data_file(DATA_FILES.board)['hash values']



# def load_initial_pieces():
# 	boarDataFilePath = os.path.join(DATA_DIRECTORY, BOARD_DATA_FILE)
# 	with open(boarDataFilePath,'r') as boardDataFile:
# 		boardData = json.load(boardDataFile)
# 	return boardData['initial pieces']
#
#
# def load_masks():
# 	maskTypes = ('rank', 'file', 'diagonal', 'antidiagonal', 'pawnBlocker')
# 	MoveMasks = namedtuple('MoveMasks', maskTypes)
#
# 	path = os.path.join(DATA_DIRECTORY, MASK_DATA_FILE)
# 	with open(path,'r') as maskFile:
# 		maskDict = json.load(maskFile, object_hook=parseJson)
# 	return MoveMasks(*[maskDict[maskType] for maskType in moveMaskTypes])
#
#
# def load_piece_index_values():
# 	boarDataFilePath = os.path.join(DATA_DIRECTORY, BOARD_DATA_FILE)
# 	with open(boarDataFilePath,'r') as boardDataFile:
# 		indexers = json.load(boardDataFile)['piece index values']
#
# 	indexerLabels = ['num pieces', 'piece type lookup',
# 					 'piece color lookup', 'color ranges']
#
# 	return (indexers[label] for label in indexerLabels)
#
# def load_hash_values():
# 	path = os.path.join(DATA_DIRECTORY, 'hashes.pickle')
# 	with open(path, 'rb') as handle:
# 		hashes = pickle.load(handle)
# 	return hashes
#
#
# def load_cached_moves():
#
# 	# converts json string representations of bitboards to integers
#
# 	movesFilePath = os.path.join(DATA_DIRECTORY, MOVE_DATA_FILE)
# 	# Load precomputed move bitboards from file
# 	with open(movesFilePath, 'r') as movesFile:
# 		moveData = json.load(movesFile, object_hook=parseJson)
# 	return moveData['moves'], moveData['move sets']
#
# def load_evaluation_data():
# 	with open('data/evaluate.json','r') as evaluationDataFile:
# 		DATA = json.load(evaluationDataFile)
# 		# convert json str keys to ints
# 		convertKeys = lambda d: [{int(k):v for k,v in table.items()} for table in d]
# 		PST_LOOKUP = [convertKeys(DATA['PST'][0]), convertKeys(DATA['PST'][1])]
#
# 		# CENTER_SQUARE_MASKS = DATA['squares']['center']
# 		# OUTER_CENTER_SQUARE_MASKS = DATA['squares']['outer-center']
# 	return PST_LOOKUP, DATA['piece values'],  #, CENTER_SQUARE_MASKS, OUTER_CENTER_SQUARE_MASKS
