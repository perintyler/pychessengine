"""
TODO make json files pickle files to properly store dicts with int keys

"""
import os
import json
from collections import namedtuple

from settings import (DATA_DIRECTORY, BOARD_DATA_FILE, MOVE_DATA_FILE,
					  MASK_DATA_FILE, EVALUATION_DATA_FILE)


isDigit = lambda k: k.lstrip('-').isdigit()
parseJson = lambda d: {int(k) if isDigit(k) else k:v for k,v in d.items()}


def load_masks():
	moveMaskTypes = ('rank','file','diagonal','antidiagonal',
					 'pawnBlocker','centerSquares','outerCenterSquares')
	MoveMasks = namedtuple('MoveMasks', moveMaskTypes)

	path = os.path.join(DATA_DIRECTORY, MASK_DATA_FILE)
	with open(path,'r') as maskFile:
		maskDict = json.load(maskFile, object_hook=parseJson)
	return MoveMasks(*[maskDict[maskType] for maskType in moveMaskTypes])

def load_board_data():
	boarDataFilePath = os.path.join(DATA_DIRECTORY, BOARD_DATA_FILE)
	with open(boarDataFilePath,'r') as boardDataFile:
		boardData = json.load(boardDataFile)

	boardDataKeys = ['hash table', 'initial piece bitboards', 'num pieces',
					 'piece type lookup', 'piece color lookup', 'color ranges']

	return (boardData[key] for key in boardDataKeys)


def load_move_data():

	# converts json string representations of bitboards to integers

	movesFilePath = os.path.join(DATA_DIRECTORY, MOVE_DATA_FILE)
	# Load precomputed move bitboards from file
	with open(movesFilePath, 'r') as movesFile:
		moveData = json.load(movesFile, object_hook=parseJson)
	return moveData['moves'], moveData['move sets']

def load_evaluation_data():
	with open('data/evaluate.json','r') as evaluationDataFile:
		DATA = json.load(evaluationDataFile)
		# convert json str keys to ints
		convertKeys = lambda d: [{int(k):v for k,v in table.items()} for table in d]
		PST_LOOKUP = [convertKeys(DATA['PST'][0]), convertKeys(DATA['PST'][1])]
		# CENTER_SQUARE_MASKS = DATA['squares']['center']
		# OUTER_CENTER_SQUARE_MASKS = DATA['squares']['outer-center']
	return PST_LOOKUP #, CENTER_SQUARE_MASKS, OUTER_CENTER_SQUARE_MASKS
