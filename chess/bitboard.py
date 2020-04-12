# -*- coding: utf-8 -*-
"""Bitboards
"""

def create(squares):
	"""bitboard factory"""
	bits = 0
	for square in squares:
		squareMask = 1 << (63-square)
		bits |= squareMask
	return bits

def reverse(bitboard):
	"""binary reversal"""
	reversedBits  = 0
	for _ in range(64):
		reversedBits <<= 1
		reversedBits |= bitboard & 1
		bitboard >>= 1
	return reversedBits

# def combine(bitboards):
# 	"""Binary Set Union"""
# 	combined = 0
# 	for bitboard in bitboards:
# 		combined |= bitboard
# 	return combined
#
