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
