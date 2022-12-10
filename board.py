from selenium import webdriver
from selenium.webdriver.common.by import By

class Board:
    size:int
    tile_count: int
    tiles: list
    browser: webdriver

    def __init__(self, browser, size=5) -> None:
        self.size = size
        self.tile_count = int((size + 1) * (3*size - 1) * 0.25)   
        self.tiles = list
        self.browser = browser

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
    
    def add_tiles(self, tiles) -> None:
        self.tiles = tiles

    def change_tiles(self, idx1, idx2) -> None:
        tile1_temp = self.tiles[idx1]
        
        self.tiles[idx1] = self.tiles[idx2]
        self.tiles[idx2] = tile1_temp

        self.tiles[idx1].update_col_pos()
        self.tiles[idx2].update_col_pos()
