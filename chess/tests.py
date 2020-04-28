# -*- coding: utf-8 -*-
"""Tests for move generation, board representation, and evaluation

Todo: everything
"""
import unittest
import chess

def state_to_char_array(state):
    return ''.join(str(state).split('\n'))

class TestMoveGeneration(unittest.TestCase):
    """ self.assertEqual(testVal, realVal) """

    def setUp(self):
        self.states = []
        self.charBoards = list(map(state_to_char_array, self.states))

    # def test_pawn_move_generation():
    #     pass

    def test_rook_move_generation():
        pass

    def test_sliding_piece_move_generation():

        pass

    def test_easy_move_generation(self):
        """ Knight and King """


        self.assertEqual(True,True)



if __name__ == '__main__':
	unittest.main()
