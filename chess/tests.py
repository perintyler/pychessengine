from bitboard import Bitboard
from random import randrange
import numpy as np

'''Todo:
    - bitboard test
    - move validation/generation test (perft)
    - state tests
        + piece iteration
        + update/pop
        + __str__
    - eval property func tests
    - search test. idk how though
'''
maxInt = 0xFFFFFFFFFFFFFFFF

class BitboardTest:

    def test_create_bitboard():
        pass
        
    # bitboard testing
    def test_count_bits():

    	for i in range(100):
    		randomBoardInt = randrange(maxInt)
    		numOnBits = bin(randomBoardInt).count('1')
    		bitboard = Bitboard(randomBoardInt)
    		count = bitboard.count_on_bits()
    		assert count == numOnBits
    	print('test on bits passed tests')

    def test_reverse():
    	for i in range(10):
    		randomBoardInt = randrange(maxInt)
    		bitStr = bin(randomBoardInt)[2:]
    		reversedBitStr = reversed(bitStr)

    		bitboard = Bitboard(randomBoardInt)
    		reversedBB = reversed(bitboard)
    		binaryStr = np.binary_repr(reversedBB.bits)
    		assert binaryStr == reversedBitStr

if __name__ == '__main__':
	pass
	# test_reverse()
	# test_is_bit_on()
