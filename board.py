from selenium import webdriver

class Board:
    size: int
    tiles: list

    def __init__(self, size: int) -> None:
        self.size = size
        self.tiles = []
        self.tile_count = int((size + 1) * (3*size - 1) * 0.25)

    def __str__(self) -> str:
        # TODO THIS IS WRONG. DOESN'T WORK FOR 7x7
        string = ''
        count = 0
        for i in range(self.size):
            if i % 2 == 0:

                temp = self.tiles[count:count+self.size]
                for i in temp:
                    print(f'{i.pos} ', end='')

                string += ' '.join(str(tile) for tile in self.tiles[count:count+self.size])
                string += '\n'
                count += 5
            else:
                a = int((self.size+1)/2)

                temp = self.tiles[count:count+a]
                for i in temp:                    
                    print(f'{i.pos} ', end='')

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


class Web_Board(Board):
    browser: object
    # browser: webdriver

    def __init__(self, browser: object, size: int) -> None:
        super().__init__(size)
        self.browser = browser

    def __repr__(self) -> str:
        return f"Board({self.size}, {self.tile_count}, {self.tiles}, {self.browser})"