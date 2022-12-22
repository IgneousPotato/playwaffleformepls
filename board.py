import numpy as np

from selenium import webdriver

class Board:
    size: int
    tiles: list
    board: list

    def __init__(self, size: int) -> None:
        self.size = size
        self.tiles = []
        self.board = np.ndarray((self.size, self.size), dtype=object)
        self.tile_count = int((size + 1) * (3*size - 1) * 0.25)

    def __str__(self) -> str:
        string = ''
        for row, tile in enumerate(self.board):
            if row % 2 == 0:
                string += ' '.join(str(t) for t in tile)
            else:
                string += '   '.join(str(t) for t in tile[::2])
            string += '\n'
        return string

    def __repr__(self) -> str:
        return f"Board({self.size}, {self.tile_count}, {self.tiles})"
    
    def add_tiles(self, tiles) -> None:
        self.tiles = tiles
        for tile in self.tiles:
            self.board[tile.pos] = tile

    def change_tiles(self, idx1, idx2) -> None:
        tile1_temp = self.tiles[idx1]
        
        self.tiles[idx1] = self.tiles[idx2]
        self.tiles[idx2] = tile1_temp

        # TODO AFTER I FINISH SOLVER NEED TO MAKE THIS WORK FOR NON-WEB VERSION 
        self.tiles[idx1].update_col_pos()
        self.tiles[idx2].update_col_pos()


class Web_Board(Board):
    browser: object
    # browser: webdriver

    def __init__(self, browser: object, size: int) -> None:
        super().__init__(size)
        self.browser = browser

    def __repr__(self) -> str:
        return f"Board({self.size}, {self.tile_count}, {self.tiles}, {self.browser})"