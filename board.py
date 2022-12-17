from selenium import webdriver

class Board:
    size: int
    tile_count: int
    tiles: list

    def __init__(self, size=5) -> None:
        self.size = size
        self.tiles = []
        self.tile_count = int((size + 1) * (3*size - 1) * 0.25)

    def __str__(self) -> str:
        string = ''
        count = 0
        for i in range(self.size):
            if i % 2 == 0:
                string += ' '.join(str(tile) for tile in self.tiles[count:count+self.size])
                string += '\n'
                count += 5
            else:
                a = int((self.size+1)/2)
                string += '   '.join(str(tile) for tile in self.tiles[count:count + a])
                string += '\n'
                count += a
        return string

    def __repr__(self) -> str:
        return f"Board({self.size}, {self.tile_count}, {self.tiles})"
    
    def add_tiles(self, tiles) -> None:
        self.tiles = tiles

    def change_tiles(self, idx1, idx2) -> None:
        tile1_temp = self.tiles[idx1]
        
        self.tiles[idx1] = self.tiles[idx2]
        self.tiles[idx2] = tile1_temp

        # TODO AFTER I FINISH SOLVER NEED TO MAKE THIS WORK FOR NON-WEB VERSION 
        self.tiles[idx1].update_col_pos()
        self.tiles[idx2].update_col_pos()


class Board(Board):
    browser: webdriver

    def __init__(self, browser, size=5) -> None:
        super().__init__(size)
        self.browser = browser

    def __repr__(self) -> str:
        return f"Board({self.size}, {self.tile_count}, {self.tiles}, {self.browser})"