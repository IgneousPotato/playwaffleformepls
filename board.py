import numpy as np

class Board:
    size: int
    tiles: list
    board: list

    def __init__(self, size: int) -> None:
        self.size = size
        self.tile_pos = self.get_pos()
        self.board = np.ndarray((self.size, self.size), dtype=object)
        self.tile_count = len(self.tile_pos)
        self.tiles = []

    def __str__(self) -> str:
        string = '\n'
        for row, tile in enumerate(self.board):
            string += '  '
            if row % 2 == 0:
                string += ' '.join(str(t) for t in tile)
            else:
                string += '   '.join(str(t) for t in tile[::2])
            string += '\n'

        return string

    def __repr__(self) -> str:
        return f"Board({self.size}, {self.tile_count}, {self.tiles})"

    def get_pos(self) -> list:
        pos = []
        for i in range(self.size):
            for j in range(self.size):
                if i % 2 != 0 and j % 2 != 0:
                    continue 
                else:
                    pos.append((i, j))
        return pos
    
    def add_tiles(self, tiles) -> None:
        self.tiles = tiles
        for i, tile in enumerate(self.tiles):
            self.board[self.tile_pos[i]] = tile

    def change_tiles(self, idx1, idx2) -> None:
        tile1_temp = self.tiles[idx1]
        
        self.tiles[idx1] = self.tiles[idx2]
        self.tiles[idx2] = tile1_temp

        self.board[self.tile_pos[idx1]] = self.tiles[idx1]
        self.board[self.tile_pos[idx2]] = self.tiles[idx2]

        self.tiles[idx1].update_colour()
        self.tiles[idx2].update_colour()


class Web_Board(Board):
    browser: object

    def __init__(self, browser: object, size: int) -> None:
        super().__init__(size)
        self.browser = browser

    def __repr__(self) -> str:
        return f"Board({self.size}, {self.tile_count}, {self.tiles}, {self.browser})"