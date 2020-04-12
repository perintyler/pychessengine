
import os
import json

from settings import (DATA_DIRECTORY, BOARD_DATA_FILE, MOVE_DATA_FILE,
                      MASK_DATA_FILE, EVALUATION_DATA_FILE, DATA_FILES)
from pregame.generate import *


GENERATION_FUNCS = {
    MOVE_DATA_FILE: generate_move_data,
    MASK_DATA_FILE: generate_masks,
    EVALUATION_DATA_FILE: generate_evaluation_data,
    BOARD_DATA_FILE: generate_board_data
}

def data_file_already_exists(fileName):
    path = os.path.join(DATA_DIRECTORY,fileName)
    return os.path.exists(path)

def is_complete():
    """Returns True if all pregame data files have been generated"""
    for fileName in DATA_FILES:
        if not data_file_already_exists(fileName):
            return False
    return True


def generate_data_and_save_to_file(fileName):
    path = os.path.join(DATA_DIRECTORY,fileName)
    if os.path.exists(path):
        prompt = f'{filePath} already exists. Delete and regenerate? (y/n)'
        shouldRegenerate = input(prompt) == 'y'
        if not shouldRegenerate: return
         # user prompted to regenerate. delete existing file
        os.remove(path)

    dataToSave = GENERATION_FUNCS[fileName]()
    with open(path,'w') as dataFile:
        json.dump(dataToSave, dataFile)
    print(f'pregame data file \'{fileName}\' created')

def save_all():
    for fileName in DATA_FILES:
        save_data_file(fileName)
