import os

from settings import DATA_FILES
import pregame

def setup_data_files():
    if pregame.is_complete():
        print('pregame setup was already previously completed. exiting setup')
        return

    # generate data for data files that don't exist
    for fileName in DATA_FILES:
        if not pregame.data_file_already_exists(fileName):
            pregame.generate_data_and_save_to_file(fileName)
    print('pregame setup has successfully completed')

if __name__ == '__main__':
    setup_data_files()
