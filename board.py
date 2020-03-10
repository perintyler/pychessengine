from color import WHITE,BLACK
from player import Player
from pieces import King # for castle
class Board:

    def __init__(self, whitePieces, blackPieces, colorToMove, **kwargs):
        self.colorToMove = colorToMove

        whitePieceTypes, whitePieceSquares = whitePieces
        blackPieceTypes, blackPieceSquares = blackPieces

        whiteKwargs, blackKwargs = {},{}
        if 'development' in kwargs:
            whiteDevelopment, blackDevelopment = kwargs['development']
            whiteKwargs['development'] = whiteDevelopment
            blackKwargs['development'] = blackDevelopment

        self.white = Player(whitePieceTypes, whitePieceSquares, WHITE, **whiteKwargs)
        self.black = Player(blackPieceTypes, blackPieceSquares, BLACK, **blackKwargs)
        
        # Create occupation bitboard representing squares occupied
        # by a piece of either color. Then, use it to create an
        # attack bitboard for each individual player
        self.occupied = self.white.occupied | self.black.occupied
        self.white.compute_attacks(self.occupied, self.black.occupied)
        self.black.compute_attacks(self.occupied, self.white.occupied)

    def get_player(self, color):
        return self.white if color == WHITE else self.black


    def moving_player_in_check(self):
        movingPlayer = self.get_player(self.colorToMove)
        enemyAttacks = self.get_player(self.colorToMove.other()).attacks 
        kingSquare = movingPlayer.king.square
        return enemyAttacks.is_bit_on(kingSquare)

    def make_move(self, move):
        activePlayer = self.get_player(self.colorToMove)
        waitingPlayer = self.get_player(self.colorToMove.other())

        activePieces,activeDevelopment = activePlayer.serialize(move=move)
        if move.isACapture:
            captureSquare = move.endSquare
            waitingPieces,waitingDevelopment = waitingPlayer.serialize(squareToRemove=captureSquare)
        else: 
            waitingPieces,waitingDevelopment = waitingPlayer.serialize()

        colorToMove = self.colorToMove.other()
        if self.colorToMove == WHITE:
            development = activeDevelopment,waitingDevelopment
            return Board(activePieces, waitingPieces, BLACK, development=development)
        else:
            development = waitingDevelopment,activeDevelopment
            return Board(waitingPieces, activePieces, WHITE, development=development)

    def prettyPrint(self, title=None, showValuation=False):
        strArr = [' ' for _ in range(64)]
        for piece in self.white.pieces:
            strArr[piece.square] = piece.as_char().upper()
        for piece in self.black.pieces:
            strArr[piece.square] = piece.as_char()

        sidePadding = ' '*50

        printStr = ''
        if title is not None:
            # title = title if not showValuation else f'{title}'
            header = sidePadding + ' * ' + title + ' *'
            printStr += header

        divider = '\n' + sidePadding + '_'*33 + '\n'
        for i in range(64):
            if i % 8 == 0:
                printStr+=divider + sidePadding + '|'
            printStr += ' ' + strArr[i] + ' |'
        printStr += divider
        print(printStr)

        



