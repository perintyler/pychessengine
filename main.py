from tree import SearchTree
from board import Board
from color import Color
import time

startingPosition = [
    'R','N','B','K','Q','B','N','R',
    'P','P','P','P','P','P','P','P',
    ' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',
    ' ',' ',' ',' ',' ',' ',' ',' ',
    'p','p','p','p','p','p','p','p',
    'r','n','b','k','q','b','n','r'
]

def main():
    whitePieceTypes, whitePieceSquares = [],[]
    blackPieceTypes, blackPieceSquares = [],[]

    for i, squareChar in enumerate(startingPosition):
        if squareChar == ' ': continue
        color = Color.WHITE if squareChar.isupper() else Color.BLACK
        squareChar = squareChar.lower()
        if color == Color.WHITE:
            whitePieceTypes.append(squareChar)
            whitePieceSquares.append(i)
        else:
            blackPieceTypes.append(squareChar)
            blackPieceSquares.append(i)



    whitePieces = whitePieceTypes, whitePieceSquares
    blackPieces = blackPieceTypes, blackPieceSquares
    board = Board(whitePieces, blackPieces, Color.WHITE)
    board.prettyPrint('Start Position', True)
    searchTree = SearchTree(board,)
    moveCount = 0
    while True:
        start = time.time()
        move,newBoard = searchTree.get_best_move()
        end = time.time()
        moveCount+=1
        newBoard.prettyPrint()
        timeElapsed = str(end - start)
        print('found move in ' + timeElapsed + ' seconds')
        # newBoard.prettyPrint(str(moveCount), True)

if __name__ == "__main__":
    # import multiprocessing as mp
    # mp.set_start_method('spawn')
    main()