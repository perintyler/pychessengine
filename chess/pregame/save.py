# -*- coding: utf-8 -*-
"""Engine Data File Management"""

import os
import json
import pickle
from collections import namedtuple

from settings import DATA_DIRECTORY

from chess.pregame.board import generate_board_data
from chess.pregame.masks import generate_masks
from chess.pregame.moves import generate_move_cache
from chess.pregame.magic import generate_magic_bitboard_cache


DataFiles = namedtuple('DataFiles', ('board', 'moves', 'masks', 'magic'))
DATA_FILES = DataFiles('board.pickle','moves.pickle','masks.pickle',' magic.pickle')

class InvalidDataFileError(Exception): pass
class MissingConfigFileError(Exception): pass

def generate_data_file(fileName):
    path = os.path.join(DATA_DIRECTORY,fileName)

    # If file already exists, prompt user if it should be deleted/regenerated
    if os.path.exists(path):
        prompt = f'{fileName} already exists. Delete and regenerate? (y/n)'
        if input(prompt) != 'y': return # Exit Generation
        os.remove(path) # delete file and regenerate

    # generate the data
    if fileName == DATA_FILES.moves:
        data = generate_move_cache()
    elif fileName == DATA_FILES.masks:
        data = generate_masks()
    elif fileName == DATA_FILES.board:
        data = generate_board_data()
    elif fileName == DATA_FILES.magic:
        data = generate_magic_bitboard_cache()
    else:
        raise InvalidDataFileError(f'Unknown data file {fileName}')

    # save the data to file. File is either a json or pickle file
    fileType = os.path.splitext(fileName)[1]
    fileMode = 'w' if fileType == '.json' else 'wb'
    with open(path, fileMode) as dataFile:
        file_lib = json if fileType == '.json' else pickle
        file_lib.dump(data, dataFile)

    print(f'pregame data file \'{fileName}\' created')

def data_is_generated():
    for fileName in DATA_FILES:
        path = os.path.join(DATA_DIRECTORY, fileName)
        if os.path.exists(path): return False
    return True

def generate_missing_data_files():
    for fileName in DATA_FILES:
        path = os.path.join(DATA_DIRECTORY, fileName)
        if os.path.exists(path): continue
        generate_data_file(fileName)
