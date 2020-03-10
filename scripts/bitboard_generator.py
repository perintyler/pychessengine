
def prettyPrint(bb,loc):
    binary = bin(bb)[2:]
    if len(binary)!=64:
    	padding = '0'*(64-len(binary))
    	binary = padding+binary
    res = ''
    for i in range(64):
        if i%8==0: res += '\n'
        if i == loc: res+= 'X'
        else: res += str(binary[i])
    print(res)

# Straight directions
def N(x,y,i): return x,y+i
def E(x,y,i): return x+i,y
def S(x,y,i): return x,y-i
def W(x,y,i): return x-i,y

# Diagonal Directions 
def NE(x,y,i): return x+i,y+i
def SE(x,y,i): return x+i,y-i
def SW(x,y,i): return x-i,y-i
def NW(x,y,i): return x-i,y+i

def diaganols(x,y):
	moves = []
	directions = [NE,SE,SW,NW]
	for distance in range(1,8):
		moves.extend([d(x,y,distance) for d in directions])
	return moves

def straights(x,y):
	moves = []
	directions = [N,E,S,W]
	for distance in range(1,8):
		moves.extend([d(x,y,distance) for d in directions])

	return moves

def get_movesForNight(x,y):
	return [
		(x+1,y+2),
		(x+1,y-2),
		(x+2,y+1),
		(x+2,y-1),
		(x-1,y+2),
		(x-1,y-2),
		(x-2,y+1),
		(x-2,y-1)
	]

def get_movesForKing(x,y):
	distance = 1
	directions = [N,NE,E,SE,S,SW,W,NW]
	return [d(x,y,distance) for d in directions]

def getMovesForBishop(x,y): return diaganols(x,y)
def getMovesForRook(x,y): return straights(x,y)
def getMovesForQueen(x,y): return diaganols(x,y) + straights(x,y)


# this is the most unique case. do later
def movesForPawn(x,y,color):
	direction = 1 if color == 'white' else -1

	nonCaptures = [(x,y+direction)]
	# if y == 1 and color == 'white' or y == 6 and color=='black':
	# 	upTwo = (x, y+2*direction)
	# 	nonCaptures.append(upTwo)

	captureLeft = (x-1, y+direction)
	captureRight = (x+1, y+direction)
	captures = [captureLeft, captureRight]
	validCaptures, validNonCaptures = [],[]
	for mx,my in nonCaptures:
		if 0<=mx<8 and 0<=my<8:
			validNonCaptures.append((mx,my))

	for mx,my in captures:
		if 0<=mx<8 and 0<=my<8:
			validCaptures.append((mx,my))
	return validCaptures, validNonCaptures
'''
Used to generate moves for every piece except pawns. 
Pawns are unique and must be dealt with seperately
'''
def get_movesForPiece(x,y,piece):
	moves = {
		'n': get_movesForNight,
		'b': get_movesForBishop,
		'r': get_movesForRook,
		'q': get_movesForQueen,
		'k': get_movesForKing
	}[piece](x,y)
	validMoves = []
	for x,y in moves: 
		if 0<=x<8 and 0<=y<8:
			validMoves.append((x,y))
	return validMoves


def createBitboard(moves):
	board = ['0' for _ in range(64)]
	for m in moves:
		x,y = m 
		i = 8*y + x
		board[i] = '1'
	boardStr = ''.join(board)
	return int(boardStr,2)

def createBitboardsForPiece(piece):# except pawns
	bitboards = []
	for i in range(64):
		ix = i%8
		iy = int((i-ix)/8)
		moves = get_movesForPiece(ix,iy,piece)
		bitboard = createBitboard(moves)
		bitboards.append(bitboard)
	return bitboards

def getPawnBitboards():
	bitboards = []
	for i in range(64):
		ix = i%8
		iy = int((i-ix)/8)
		capturesWhite, nonCapturesWhite = movesForPawn(ix,iy,'white')
		capturesBlack, nonCapturesBlack = movesForPawn(ix,iy,'black')

		captureBitboardsWhite = createBitboard(capturesWhite)
		nonCaptureBitboardsWhite = createBitboard(nonCapturesWhite)
		whiteBitboards = [captureBitboardsWhite, nonCaptureBitboardsWhite]

		captureBitboardsBlack = createBitboard(capturesBlack)
		nonCaptureBitboardsBlack = createBitboard(nonCapturesBlack)
		blackBitboards = [captureBitboardsBlack, nonCaptureBitboardsBlack]

		bitboardsForSquare = [whiteBitboards, blackBitboards]
		bitboards.append(bitboardsForSquare)
	return bitboards

def saveBitboardsToFile():
	pieces = ['n','b','r','q','k']
	file_dict = {}
	for p in pieces:
		file_dict[p] = createBitboardsForPiece(p)

	file_dict['p'] = getPawnBitboards()
	file_dir = 'data'
	file_name = 'move_bitboards.json'
	file_path = file_dir + '/' + file_name
	# file_path = f'{file_dir}/{file_name}'

	import json
	with open(file_path, 'w') as file:
		json.dump(file_dict, file)


if __name__ == '__main__':
	saveBitboardsToFile()
		#saveBitboardsToFile()
