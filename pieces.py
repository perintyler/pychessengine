import sys
from move_generation import get_hashed_moves, get_straight_moves, get_diagonal_moves
from color import WHITE, BLACK

class Piece:

	def __init__(self, square, color):
		self.square = square
		self.color = color
		self.moves = None

	def get_moves(self, board):
		assert board.occupied is not None
		ownBitboard = board.get_player(self.color).occupied
		enemyBitboard = board.get_player(self.color.other()).occupied
		allMoves = self.get_move_bitboard(board)
		captures = allMoves & enemyBitboard
		nonCaptures = allMoves & ~ownBitboard & ~captures
		return captures, nonCaptures

	# used to create attack bitboards. Wraps the get_move_bitboard
	# function for the sake of clarity outside this file
	def get_pseudo_legal_moves(self, occupied):
		return self.get_move_bitboard(occupied)

	def update_square(self, square):
		self.square = square

	def get_move_bitboard(self, occupied):
		if self.moves is None:
			self.moves = self.create_move_bitboard(occupied)
		return self.moves

	def create_move_bitboard(self, occupied):
		pass

	def get_value(self):
		pass

	def as_char(self):
		pass

	def as_int(self):
		pass




class Pawn(Piece):

	def get_moves(self, board):
		if self.moves is None:
			self.create_move_bitboard()

		captures, nonCaptures = self.moves
		startingRank = 1 if self.color == WHITE else 6
		currentRank = self.square // 8
		occupied = board.occupied
		
		if startingRank == currentRank:
			currentFile = self.square % 8
			direction = 1 if self.color == WHITE else -1
			rankAbove = currentRank+direction
			squareInFront = (rankAbove)*8 + currentFile

			if not occupied.is_bit_on(squareInFront):
				upTwo = currentRank + 2*direction
				twoSquaresInFront = (upTwo)*8 + currentFile
				nonCaptures.turn_on_bit(twoSquaresInFront)
		enemyColor = self.color.other()
		enemyBitboard = board.get_player(enemyColor).occupied
		validCaptures = captures & enemyBitboard
		ownBitboard = board.get_player(self.color).occupied
		validNonCaptures = 	nonCaptures & ~ownBitboard
		return validCaptures, validNonCaptures
	
	def create_move_bitboard(self, occupied):		
		captures, nonCaptures = get_hashed_moves('p',self.square,self.color)
		self.moves = captures, nonCaptures

	def get_pseudo_legal_moves(self, occupied):
		if self.moves is None:
			self.create_move_bitboard(occupied)
		captures, nonCaptures = self.moves 
		return captures

	def get_value(self):
		return 1

	def as_char(self):
		return 'p'

	def as_int(self):
		return 1

class Bishop(Piece):

	def create_move_bitboard(self, occupied):
		return get_diagonal_moves(self.square, occupied)

	def get_value(self):
		return 3

	def as_char(self):
		return 'b'

	def get_initial_square(self):
		if self.color == WHITE:
			return 

	def as_int(self):
		return 3

class Knight(Piece):

	def create_move_bitboard(self, occupied):
		return get_hashed_moves('n', self.square)

	def get_value(self):
		return 3

	def as_char(self):
		return 'n'

	def as_int(self):
		return 2

class Rook(Piece):

	WHITE_SQUARES = (0,7)
	BLACK_SQUARES = (56,63)

	@staticmethod
	def get_start_square(color, onKingSide):
		whiteSquares,blackSquares = Rook.WHITE_SQUARES,Rook.BLACK_SQUARES
		kingSide,queenSide = whiteSquares if color==WHITE else blackSquares
		return kingSide if onKingSide else queenSide

	def create_move_bitboard(self, occupied):
		return get_straight_moves(self.square, occupied)

	def get_value(self):
		return 5

	def as_char(self):
		return 'r'

	def as_int(self):
		return 3

class Queen(Piece):

	def create_move_bitboard(self, occupied):
		straightMoves = get_straight_moves(self.square, occupied)
		diagonalMoves = get_diagonal_moves(self.square, occupied)
		return straightMoves | diagonalMoves

	def get_value(self):
		return 9

	def as_char(self):
		return 'q'

	def as_int(self):
		return 4

class King(Piece):

	WHITE_START_SQUARE = 3
	BLACK_START_SQUARE = 59

	@staticmethod
	def get_start_square(color):
		if color == WHITE:
			return King.WHITE_START_SQUARE
		else:
			return King.BLACK_START_SQUARE

	def get_moves(self, board):
		enemyColor = self.color.other()
		enemyPlayer = board.get_player(enemyColor)

		threatened = enemyPlayer.attacks
		friends = board.get_player(self.color).occupied
		enemies = enemyPlayer.occupied
		allMoves = self.create_move_bitboard(board)
		allMoves = allMoves & ~threatened
		captures = allMoves & enemies
		nonCaptures = allMoves & ~friends & ~enemies
		return captures, nonCaptures

	def create_move_bitboard(self, occupied):
		return get_hashed_moves('k', self.square)

	def get_value(self):
		return sys.maxsize

	def as_char(self):
		return 'k'

	def as_int(self):
		return 5

pieceTypes = {
	'p': Pawn,
	'n': Knight,
	'b': Bishop,
	'r': Rook,
	'q': Queen,
	'k': King
}

def create(pieceChar, square, color):
	return pieceTypes[pieceChar](square, color)
Piece.create = create

