from tests import test_board
from tests import test_moves
from tests import test_search
from tests import test_evaluate

def run_all_tests():
  test_board.test_occupancy_bitboards()
  test_board.test_zobrist_hashing()
  test_board.test_update()
