from chess.pregame.board import (Bitboard, count_bits, reverse_bitboard,
                                 get_square, get_coordinate, parse_notation,
                                 get_squares_from_bitboard)
from chess.pregame.moves import get_rays,N,NE,E,SE,S,SW,W,NW
from chess.pregame.masks import generate_ray_masks

ROOK_MAGICS = [
    0xa8002c000108020,0x6c00049b0002001,0x100200010090040,0x2480041000800801,
    0x280028004000800,0x900410008040022,0x280020001001080,0x2880002041000080,
    0xa000800080400034,0x4808020004000,0x2290802004801000,0x411000d00100020,
    0x402800800040080,0xb000401004208,0x2409000100040200,0x1002100004082,
    0x22878001e24000,0x1090810021004010,0x801030040200012,0x500808008001000,
    0xa08018014000880,0x8000808004000200,0x201008080010200,0x801020000441091,
    0x800080204005,0x1040200040100048,0x120200402082,0xd14880480100080,
    0x12040280080080,0x100040080020080,0x9020010080800200,0x813241200148449,
    0x491604001800080,0x100401000402001,0x4820010021001040,0x400402202000812,
    0x209009005000802,0x810800601800400,0x4301083214000150,0x204026458e001401,
    0x40204000808000,0x8001008040010020,0x8410820820420010,0x1003001000090020,
    0x804040008008080,0x12000810020004,0x1000100200040208,0x430000a044020001,
    0x280009023410300,0xe0100040002240,0x200100401700,0x2244100408008080,
    0x8000400801980,0x2000810040200,0x8010100228810400,0x2000009044210200,
    0x4080008040102101,0x40002080411d01,0x2005524060000901,0x502001008400422,
    0x489a000810200402,0x1004400080a13,0x4000011008020084,0x26002114058042
]

BISHOP_MAGICS = [
    0x89a1121896040240,0x2004844802002010,0x2068080051921000,0x62880a0220200808,
    0x4042004000000,0x100822020200011,0xc00444222012000a,0x28808801216001,
    0x400492088408100,0x201c401040c0084,0x840800910a0010,0x82080240060,
    0x2000840504006000,0x30010c4108405004,0x1008005410080802,0x8144042209100900,
    0x208081020014400,0x4800201208ca00,0xf18140408012008,0x1004002802102001,
    0x841000820080811,0x40200200a42008,0x800054042000,0x88010400410c9000,
    0x520040470104290,0x1004040051500081,0x2002081833080021,0x400c00c010142,
    0x941408200c002000,0x658810000806011,0x188071040440a00,0x4800404002011c00,
    0x104442040404200,0x511080202091021,0x4022401120400,0x80c0040400080120,
    0x8040010040820802,0x480810700020090,0x102008e00040242,0x809005202050100,
    0x8002024220104080,0x431008804142000,0x19001802081400,0x200014208040080,
    0x3308082008200100,0x41010500040c020,0x4012020c04210308,0x208220a202004080,
    0x111040120082000,0x6803040141280a00,0x2101004202410000,0x8200000041108022,
    0x21082088000,0x2410204010040,0x40100400809000,0x822088220820214,
    0x40808090012004,0x910224040218c9,0x402814422015008,0x90014004842410,
    0x1000042304105,0x10008830412a00,0x2520081090008908,0x40102000a0a60140
]

ROOK_INDEX_BITS = [
    12, 11, 11, 11, 11, 11, 11, 12,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    11, 10, 10, 10, 10, 10, 10, 11,
    12, 11, 11, 11, 11, 11, 11, 12
]

BISHOP_INDEX_BITS = [
    6, 5, 5, 5, 5, 5, 5, 6,
    5, 5, 5, 5, 5, 5, 5, 5,
    5, 5, 7, 7, 7, 7, 5, 5,
    5, 5, 7, 9, 9, 7, 5, 5,
    5, 5, 7, 9, 9, 7, 5, 5,
    5, 5, 7, 7, 7, 7, 5, 5,
    5, 5, 5, 5, 5, 5, 5, 5,
    6, 5, 5, 5, 5, 5, 5, 6
]

def create_ray_mask(square, *directions):
    x,y = get_coordinate(square)
    coords = get_rays(x,y,directions)
    squares = [get_square(x,y) for x,y in coords if 0<=x<8 and 0<=y<8]
    return Bitboard(*squares)


def generate_attack_masks():
    """Creates rook and bishop attack masks withot edge attacks"""
    # create edge rays
    FIRST_SQUARE,LAST_SQUARE = map(parse_notation,['A1','H8'])
    RANK8 = create_ray_mask(0,E)  | Bitboard(0)
    RANK1 = create_ray_mask(63,W) | Bitboard(63)
    FILEA = create_ray_mask(0,N)  | Bitboard(0)
    FILEH = create_ray_mask(63,S) | Bitboard(63)
    EDGES = RANK8 | RANK1 | FILEA | FILEH

    rookMasks,bishopMasks = {},{}
    for square in range(64):
        squareMask = Bitboard(square)

        # straight rays without their fist/last square (edges)
        rookMasks[squareMask] = create_ray_mask(square,W) & ~FILEA \
                              | create_ray_mask(square,E) & ~FILEH \
                              | create_ray_mask(square,N) & ~RANK1 \
                              | create_ray_mask(square,S) & ~RANK8 \
                              & ~squareMask

        # diagonal rays without first/last square (edges)
        bishopMasks[squareMask]  = create_ray_mask(square, NE,SW,SE,NW) \
                                 & ~EDGES & ~squareMask


    return bishopMasks, rookMasks

def subtract_blockers(slider, occupied, mask):
  """Blocker subtraction by calculation

    Slow sliding piece move generation with o ^ (o - 2s) algorith. Used
    to  used to precompute magic tables

    https://www.chessprogramming.org/Subtracting_a_Rook_from_a_Blocking_Piece
    """

  # calculate positive rays
  potentialBlockers = occupied & mask
  positiveRay = occupied ^ (potentialBlockers - (slider*2)) # o-2s
  positiveRay = positiveRay & mask

  # reverse the Bitboards, then get negative rays
  occupiedReversed = reverse_bitboard(occupied)
  maskReversed = reverse_bitboard(mask)
  sliderReversed = reverse_bitboard(slider)

  potentialBlockers = occupiedReversed & maskReversed
  negativeRay = occupiedReversed ^ (potentialBlockers - (sliderReversed*2))
  negativeRay = reverse_bitboard(negativeRay & maskReversed)

  # combine positive and negative rays into one Bitboard
  return positiveRay | negativeRay

def create_magic_bitboard_tables():
    bishopAttacks, rookAttacks = generate_attack_masks()

    rookTable,bishopTable = {},{}

    def generate_blockers(numIndecies, attackMask):
        attackSquares = get_squares_from_bitboard(attackMask)
        for blockerIndex in range(1 << numIndecies):
            blockers = 0
            for i in range(len(attackSquares)):
                if blockerIndex & (1 << i):
                    blockers |= Bitboard(attackSquares[i])
                # if blockerIndex & (1 << i):
                #     blockers |= (1 << attackSquares[i])
            yield blockers

    for square in range(64):
        squareMask = Bitboard(square)
        # BISHOP
        bishopTable[squareMask] = {}
        numBishopIndecies = BISHOP_INDEX_BITS[square]
        bishopMagic = BISHOP_MAGICS[square]
        for blockerMask in generate_blockers(numBishopIndecies,
                                             bishopAttacks[squareMask]):
            diagonal = create_ray_mask(square, NE, SW)
            antidiagonal = create_ray_mask(square, SE, NW)

            attacks = subtract_blockers(squareMask, blockerMask, diagonal) \
                    | subtract_blockers(squareMask, blockerMask, antidiagonal)


            bishopKey = (blockerMask * bishopMagic) >> (64 - numBishopIndecies)

            bishopTable[squareMask][bishopKey] = attacks

        # ROOK
        rookTable[squareMask] = {}
        numRookIndecies = ROOK_INDEX_BITS[square]
        for blockerMask in generate_blockers(numRookIndecies,
                                             rookAttacks[squareMask]):

            rank = create_ray_mask(square, E, W)
            file = create_ray_mask(square, N, S)

            attacks = subtract_blockers(squareMask, blockerMask, rank) \
                    | subtract_blockers(squareMask, blockerMask, file)

            rookMagic = ROOK_MAGICS[square]
            rookKey = (blockerMask * rookMagic) >> (64 - numRookIndecies)

            rookTable[squareMask][rookKey] = attacks


    return bishopTable, rookTable


def generate_magic_bitboard_cache():
    bishopMagicBitboards,rookMagicBitboards = {},{}
    bishopIndexBits,rookIndexBits = {},{}
    for square in range(64):
        squareMask = Bitboard(square)

        bishopMagicBitboards[squareMask] = BISHOP_MAGICS[square]
        rookMagicBitboards[squareMask] = ROOK_MAGICS[square]

        bishopIndexBits[squareMask] = BISHOP_INDEX_BITS[square]
        rookIndexBits[squareMask] = ROOK_INDEX_BITS[square]

    bishopAttackMasks,rookAttackMasks = generate_attack_masks()
    bishopTable,rookTable = create_magic_bitboard_tables()

    return {
        'bishop': (bishopTable, bishopMagicBitboards,
                   bishopAttackMasks, bishopIndexBits),
        'rook': (rookTable, rookMagicBitboards,
                 rookAttackMasks, rookIndexBits)
    }
