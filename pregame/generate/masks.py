
from chess.bitboard import create as create_bitboard
from pregame.utils import get_square, get_coordinate

SQUARES = (
	A1, B1, C1, D1, E1, F1, G1, H1,
	A2, B2, C2, D2, E2, F2, G2, H2,
	A3, B3, C3, D3, E3, F3, G3, H3,
	A4, B4, C4, D4, E4, F4, G4, H4,
	A5, B5, C5, D5, E5, F5, G5, H5,
	A6, B6, C6, D6, E6, F6, G6, H6,
	A7, B7, C7, D7, E7, F7, G7, H7,
	A8, B8, C8, D8, E8, F8, G8, H8,
) = range(64)
WHITE,BLACK = 0,1



# ordered top right to bottom left
diagonalMaskList = [
	0x8000000000000000,
	0x4080000000000000,
	0x2040800000000000,
	0x1020408000000000,
	0x810204080000000,
	0x408102040800000,
	0x204081020408000,
	0x102040810204080,
	0x1020408102040,
	0x10204081020,
	0x102040810,
	0x1020408,
	0x10204,
	0x102,
	0x1,
]

# ordered top left to bottom right
antiDiagonalMaskList = [
	0x100000000000000,
	0x201000000000000,
	0x402010000000000,
	0x804020100000000,
	0x1008040201000000,
	0x2010080402010000,
	0x4020100804020100,
	0x8040201008040201,
	0x80402010080402,
	0x804020100804,
	0x8040201008,
	0x80402010,
	0x804020,
	0x8040,
	0x80,
]

def generate_ray_masks():
	"""Generates file, rank, diagonal, and antidiagonal masks

	Example Diagonal Mask       Example Antidiagonal Mask

		00000010                        10000000
		00000100                        01000000
		00001000                        00100000
		00100000                        00010000
		01000000                        00001000
		10000000                        00000100
		00000000                        00000010
		00000000                        00000001

	Example File Mask               Example Rank Mask

		00000010                        00000000
		00000010                        11111111
		00000010                        00000000
		00000010                        00000000
		00000010                        00000000
		00000010                        00000000
		00000010                        00000000
		00000010                        00000000
	"""
	# create a mask for each rank
	rankMaskList = []
	for rank in range(8):
		rankStartIndex = rank*8
		rankSquares = range(rankStartIndex,rankStartIndex+8)
		rankMask = create_bitboard(rankSquares)
		rankMaskList.append(rankMask)

	# create a mask for each file
	fileMaskList = []
	for file in range(8):
		fileSquares = range(file,64,8)
		fileMask = create_bitboard(fileSquares)
		fileMaskList.append(fileMask)

	maskLists = [rankMaskList,fileMaskList,
					diagonalMaskList,antiDiagonalMaskList]

	# iterate through each square on the board and add the rank, file,
	# diagonal, and antidiagonal masks that the square is a part of. This
	# way, a square's mask index does not need to be computed for retreival
	maskDicts = (rankMasks,
	 			 fileMasks,
	 		 	 diagonalMasks,
	 		 	 antiDiagonalMasks) = {},{},{},{}

	for square in SQUARES:
		fileIndex,rankIndex = get_coordinate(square)
		diagonalIndex = (square // 8) + (square % 8)
		antiDiagonalIndex = (square // 8) + 7 - (square % 8)
		maskIndecies = [fileIndex, rankIndex,
						diagonalIndex, antiDiagonalIndex]

		bitboardForSquare = create_bitboard([square])
		for dict,list,index in zip(maskDicts, maskLists, maskIndecies):
			dict[bitboardForSquare] = list[index]

	return maskDicts

def generate_center_square_masks():
	"""TODO: add example"""
	centerSquares 	   = [E4, D4, E5, D5]
	outerCenterSquares = [F3, F4, F5, F6, C3,C4, C5, C6, E3, D3, E6, D6]

	return (
		[create_bitboard([square]) for square in centerSquares],
		[create_bitboard([square]) for square in outerCenterSquares]
	)

def generate_pawn_blocker_masks():
	"""Generates single population bitboards for piece in front of each square
	TODO: ADD EXAMPLE
	"""
	def create_blocker(square, direction):
		x,y = get_coordinate(square)
		blockerSquare = get_square(x,y+direction)
		return create_bitboard([blockerSquare]) if 0<=blockerSquare<64 else 0

	pawnBlockerMasks = [{},{}]
	for square in SQUARES:
		squareBitboard = create_bitboard([square])
		pawnBlockerMasks[WHITE][squareBitboard] = create_blocker(square,1)
		pawnBlockerMasks[BLACK][squareBitboard] = create_blocker(square,-1)

	return pawnBlockerMasks


def generate_castle_masks():
	"""Generates a bitboard for castle square for each castle type
	TODO: ADD EXAMPLE
	"""
	queensideCastleSquares = {
		WHITE: [D1, C1, B1],
		BLACK: [D8, C8, B8]
	}
	kingsideCastleSquares = {
		WHITE: [F1, G1],
		BLACK: [F8, G8]
	}

	queensideMasks = map(create_bitboard, queensideCastleSquares.values())
	kingsideMasks =  map(create_bitboard, kingsideCastleSquares.values())

	return {
		'queenside': list(queensideMasks),
		'kingside': list(kingsideMasks)
	}

def generate_masks():
    # create masks and return the dict
    rankMasks,fileMasks,diagonalMasks,antiDiagonalMasks = generate_ray_masks()
    centerSquareMask, outerCenterSquareMask = generate_center_square_masks()
    pawnBlockerMasks = generate_pawn_blocker_masks()
    castleSquaresMasks = generate_castle_masks()

    return {
    	'rank': rankMasks,
    	'file': fileMasks,
    	'diagonal': diagonalMasks,
    	'antidiagonal': antiDiagonalMasks,
    	'pawnBlocker': pawnBlockerMasks,
    	'centerSquares': centerSquareMask,
    	'outerCenterSquares': outerCenterSquareMask,
    	'castleSquares': castleSquaresMasks
    }
