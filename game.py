
from tree import SearchTree
from board import Board
from color import Color
import time
from move_generation import Move



from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def parseNotation(notation):
	rankStr,fileStr = notation[0],notation[1]
	rankDict = {s:i for i,s in enumerate('abcdefgh')}
	rankInt = 7 - rankDict[rankStr]
	fileInt = int(fileStr)-1
	return fileInt*8 + rankInt

def toNotation(square):
	x = 7-(square % 8)
	y = (square // 8)
	rankStr = 'abcdefgh'[x]
	fileStr = str(y+1)
	return rankStr + fileStr

def createMoveFromNotation(board,startStr,endStr):
	startSquare = parseNotation(startStr)
	endSquare = parseNotation(endStr)
	piece = board.get_player(board.colorToMove).get_piece(startSquare)
	assert piece is not None

	enemyPlayer = board.get_player(board.colorToMove.other())
	isACapture = enemyPlayer.get_piece(endSquare) is not None
	return Move(piece, endSquare, isACapture)


def get_start_board():
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
	return Board(whitePieces, blackPieces, Color.WHITE)


def updateBoard(board, startStr, endStr):
	move = createMoveFromNotation(board, startStr, endStr)
	return board.make_move(move)

games = {}
gameTimers = {}

def check_game_status(gameId):
	timer, timeSinceMove = gameTimers[gameId]
	if timeSinceMove - time.time() > 60*10:
		del games[gameId]
		timer.stop()
		del gameTimers[gameId]

def new_game(gameId):
	print('here')
	board = get_start_board()
	tree = SearchTree(board)
	games[gameId] = tree
	print('starting game with id ' + str(gameId))
	# check game status every 10 minutes. if move hasn't 
	# been made in 5 minutes, delete it
	rt = RepeatedTimer(10*60, check_game_status, gameId)

	gameTimers[gameId] = (rt, time.time())

class GameDeletedException(Exception):
	pass

def handle_move_and_respond(gameId, startStr, endStr):
	global games
	if gameId not in games:
		raise GameDeletedException()
	print('recieved move ' + startStr + ',' + endStr + ' for game with id ' + gameId)
	tree = games[gameId]
	board = tree.root.board
	move = createMoveFromNotation(board, startStr, endStr)
	board = tree.update_with_move(move)
	board.prettyPrint()
	# tree.printValueTemps()
	start = time.time()
	move,board = tree.get_best_move()
	end = time.time()
	timeElapsed = str(end - start)
	print('found move in ' + timeElapsed + ' seconds')
	board.prettyPrint(gameId)
	startNotation = toNotation(move.piece.square)
	destNotation = toNotation(move.endSquare)

	global gameTimers
	timer, timeSinceMove = gameTimers[gameId]
	gameTimers[gameId] = (timer, time.time())

	return startNotation, destNotation
    # newBoard.prettyPrint(str(moveCount), True)
