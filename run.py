# -*- coding: utf-8 -*-
"""Engine Entry Point"""

import settings
import chess

def main():
    chess.setup()

    if settings.COMPUTER_PLAY:
        chess.play_computer_game()
    else:
        chess.play_against_computer()


if __name__ == "__main__":
    main()
