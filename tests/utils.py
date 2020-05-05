import chess
import random

def state_to_char_array(state):
    return ''.join(str(state).split('\n'))

def get_random_move(state):
    generator = chess.moves.Generator()
    attacks,attackSet = generator.find_attacks(state)
    moves = generator.find_moves(state, attacks,attackSet)
    randomMoveNumber = random.randrange(len(moves))
    for _ in range(randomMoveNumber): moves.pop()
    return moves.pop()

def get_all_moves(state):
    generator = chess.moves.Generator()
    attacks,attackSet = generator.find_attacks(state)
    moves = generator.find_moves(state, attacks,attackSet)
    moveList = []
    while len(moves)>0:
      moveList.append(moves.pop())
    return moveList
