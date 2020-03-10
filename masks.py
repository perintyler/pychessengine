# masks.py
# --------------------------------------------------------------
# This file contains binary masks which can isolate ranks, files
# diagonals, and anti-dagonals on a bitboard (see bitboard.py).
# The masks are used to generate moves for sliding pieces (see
# move_generation.py). They are also used for some aspects of 
# positional evaluation, such as finding doubled pawns. Masks
# should be obtained using the getter functions at the bottom 
# of this file, which return bitboard objects.
# ---------------------------------------------------------------


#################################################################
# DIAGONAL MASKS                                                #        
#################################################################

diagonalMasks = [
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

antiDiagonalMasks = [
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


#################################################################
# RANK AND FILE MASK                                            #        
#################################################################

def create_ranks_masks():
    masks = []
    for i in range(8):
        mask = ['0' for _ in range(64)]
        rankStart = i*8
        rankEnd = rankStart+8
        for i in range(rankStart, rankEnd):
            mask[i] = '1'
        binaryMask = int(''.join(mask),2)
        # rank_Bitboard = Bitboard(binary)
        masks.append(binaryMask)
    return masks

def create_file_masks():
    masks = []
    for i in range(8):
        mask = ['0' for _ in range(64)]
        for i in range(i,64,8):
            mask[i] = '1'
        binaryMask = int(''.join(mask),2)
        # col_Bitboard = Bitboard(binary)
        masks.append(binaryMask)  
    return masks

rankMasks = create_ranks_masks()
fileMasks = create_file_masks()


#################################################################
# MASK GETTER FUNCTIONS                                         #        
#################################################################

from bitboard import Bitboard

# ordered from left to right
def get_rank_mask(index):
    rank = index // 8
    binaryMask = rankMasks[rank]
    return Bitboard(binaryMask)

# ordered from bottom to top
def get_file_mask(index):
    file = index%8
    binaryMask = fileMasks[file]
    return Bitboard(binaryMask)

# ordered top right to bottom left 
def get_diagonal_mask(index):
    diagonalIndex = (index // 8) + (index % 8)
    binaryMask = diagonalMasks[diagonalIndex]
    return Bitboard(binaryMask)

# ordered top left to bottom right
def get_antidiagonal_mask(index):
    antiDiagonalIndex = (index // 8) + 7 - (index % 8)
    binaryMask = antiDiagonalMasks[antiDiagonalIndex]
    return Bitboard(binaryMask)
