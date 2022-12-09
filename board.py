import logging

import numpy as np

class Board:
    tile_count = int
    board: dict

    def __init__(self, size=5) -> None:
        self.tile_count = int((size + 1) * (3*size - 1) * 0.25)       
        for i in range(self.tile_count):
            self.board[i] = None
