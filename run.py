

def play():
    from chess import board,search
    import time

    state = board.State.INITIAL

    while True:
        print(state)
        start = time.time()
        state = search.for_best_move(state)
        end = time.time()
        print('found move in ' + str(end - start) + ' seconds')

if __name__ == "__main__":
    # import multiprocessing as mp
    # mp.set_start_method('spawn')

    import pregame

    if not pregame.is_complete():
        from setup import setup_data_files
        setup_data_files()
    play()
