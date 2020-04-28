# -*- coding: utf-8 -*-
"""Engine Entry Point"""

import settings
import chess
from tests import run_all_tests


def start():
  chess.pregame.setup()

  if settings.DEBUG:
    run_all_tests()

  if settings.COMPUTER_PLAY:
    chess.play_computer_game()
  else:
    chess.play_against_computer()

if __name__ == "__main__":
  start()
