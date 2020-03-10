# bitboard.py
# --------------------------------------------------------------
# This file contains the Bitboard class which is used for move 
# generation and positional evaluation. A bitboard is a binary 
# board representation, where each individual bits corresponds 
# to a square on the board. Bitboards are powerful because they
# can be manipulated using bitwise operations to perform tasks
# that would otherwise be very computationally expensive.
# --------------------------------------------------------------


class Bitboard:

    # used to ensure Bitboard has a maximum of 64 bits
    overflowMask = 0xFFFFFFFFFFFFFFFF

    def __init__(self, binary):
        self.binary = binary
  
    def get_on_bits(self):
        for index in range(64):
            mask = 1 << (63-index)
            if mask & self.binary != 0:
                yield index
    
    def count_on_bits(self):
        count = 0
        while(self.binary):
            self.binary &= self.binary - 1
            count += 1
        return count
    
    def is_bit_on(self, index):
        mask = 1 << (63-index)
        return mask & self.binary != 0
    
    def turn_on_bit(self, index):
        mask = 1 << (63-index)
        self.binary = self.binary | mask

    def __add__(self, other):
        result = self.binary + other.binary
        return Bitboard(result & Bitboard.overflowMask)

    def __sub__(self, other):
        result = self.binary - other.binary
        return Bitboard(result & Bitboard.overflowMask)

    def __mul__(self, other):
        if isinstance(other, int):
            result = self.binary * other
        else:
            result = self.binary * other.binary
        return Bitboard(result & Bitboard.overflowMask)

    def __xor__(self, other):
        result = self.binary ^ other.binary
        return Bitboard(result & Bitboard.overflowMask)

    def __or__(self, other):
        result = self.binary | other.binary
        return Bitboard(result & Bitboard.overflowMask)

    def __and__(self, other):
        result = self.binary & other.binary
        return Bitboard(result & Bitboard.overflowMask)
    
    def __invert__(self):
        return Bitboard(~self.binary)

    
    def __reversed__(self):
        n = self.binary
        result = 0
        for i in range(64):
            result <<= 1
            result |= n & 1
            n >>= 1
        return Bitboard(result)

    def prettyPrint(self, title=None):
        # get binary str from in and strip leading 0b 
        binStr = bin(self.binary)[2:]

        # add leading 0 paddings to ensure the binary has 64 bits
        binStrLength = len(binStr)
        if binStrLength < 64:
            numLeadingZeros = 64 - binStrLength
            padding = '0'*numLeadingZeros
            binStr = padding + binStr

        # print binary string as 8 by 8 grid
        printStr = ''
        if title is not None: printStr += '\t* ' + title + ' *'
        for i in range(64):
            if i%8==0: printStr += '\n'
            printStr += binStr[i]
        print(printStr)  
