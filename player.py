# player.py
# --------------------------------------------------------------
# This file contains a Player class which stores piece data for   
# either white or black and provides functionality used to evaluate
# positions. Game data is maintained with a piece centric approach, 
# wich stores lists of self contained pieces that store their own 
# locations on the board. When a Player object is instantiated,
# square centric board representatins are created in the form of
# bitboard (see bitboard.py) to store attacks and occupied squares.
# --------------------------------------------------------------

from bitboard import Bitboard
from pieces import Piece, Rook, King
from color import WHITE

class Player:

    def __init__(self, pieceTypes, squares, color, **kwargs):

        self.color = color

        # valuation components
        self.numCenterAttacks = None
        self.connectivity = None
        self.pressureCount = 0
        # bitboards
        self.occupied = Bitboard(0)
        self.attacks = Bitboard(0)
        self.pawns = Bitboard(0)

        self.pieces = []
        numBishops = 0
        for pieceType, square in zip(pieceTypes, squares):
            piece = Piece.create(pieceType, square, color)
            if piece.as_char() == 'p':
                self.pawns.turn_on_bit(piece.square)
            elif piece.as_char() == 'b':
                numBishops+=1
            elif piece.as_char() == 'k':
                self.king = piece
            self.pieces.append(piece)

        self.hasBishopPair = numBishops == 2
        self.create_occupancy_bitboard()

        # Development Bitboard tracks if a piece has moved from its initial
        # square. It is used for evaluation and determining castling rights 
        if 'development' in kwargs:
            self.development = kwargs['development']
        else:
            self.development = Bitboard(0)

    def create_occupancy_bitboard(self):
        for piece in self.pieces:
            self.occupied.turn_on_bit(piece.square)


    # For the sake of efficiency, this method has a few
    # responsibilities. 1) It creates a bitboard with an on
    # bit at every square that is attacked by this players
    # pieces. 2) It counts the amount of attacks on center
    # squares, which is used to quantify center control
    # on evaluation. 3) It counts the amount of attacks
    # on squares occupied by own pieces, which is used 
    # to quantify connectivity on evaluation.
    def compute_attacks(self, occupied, enemyPieces):
        self.numCenterAttacks = self.connectivity = 0
        D4,E4,D5,E5 = 27,28,35,36
        centerSquares = [D4,E4,D5,E5]

        for piece in self.pieces:
            # add piece attacks to attack bitboard
            attacksForPiece = piece.get_pseudo_legal_moves(occupied)
            self.attacks |= piece.get_pseudo_legal_moves(occupied)

            # count how many center squares are attacked 
            for square in centerSquares:
                if attacksForPiece.is_bit_on(square) == True:
                    self.numCenterAttacks += 1

            attackedEnemies = (enemyPieces & attacksForPiece)
            self.pressureCount += attackedEnemies.count_on_bits()
            # get union of attacks and occupied. The amount
            # of on bits will be the amount of pieces being
            # defended by this piece
            defendedPiecesBitboard = attacksForPiece & self.occupied
            self.connectivity += defendedPiecesBitboard.count_on_bits()

    # Converts piece data into lists used to instantiate
    # new board objects. If a move or capture index is given, 
    # the pieces are updated accordingly. Pawn promotion 
    # logic occurs here
    def serialize(self, move=None, squareToRemove=None):
        development = Bitboard(self.development.binary)
        if move is not None:
            development.turn_on_bit(move.startSquare)
        pieceTypes,squares = [],[]
        for piece in self.pieces:
            if squareToRemove is not None and piece.square == squareToRemove:
                continue
            elif move is not None and piece.square == move.startSquare:
                squares.append(move.endSquare)
                if self._is_move_promotion(move):
                    pieceTypes.append('q')
                    continue
            else:
                squares.append(piece.square)
            pieceTypes.append(piece.as_char())
        return (pieceTypes, squares), development

    def _is_move_promotion(self, move):
        if move.piece.as_char() != 'p': return False
        lastRank = 7 if self.color == WHITE else 0
        pieceRank = move.endSquare // 8
        return pieceRank == lastRank


    def get_development(self):
        return Bitboard(self.development.binary)

    def get_piece(self,square):
        for piece in self.pieces:
            if piece.square == square:
                return piece
        return None