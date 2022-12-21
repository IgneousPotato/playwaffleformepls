import logging

from tile import Tile
from board import Board
from solver import Solver

def read_file(file_name):
    pass

def test_archive_37():
    size = 5
    
    letters = ['Q', 'T', 'G', 'U', 'L', 'Y', 'U', 'G', 'D', 'U', 'I', 'O', 'E', 'T', 'N', 'E', 'N', 'E', 'I', 'L', 'Y']
 
    colours = ['green', 'white', 'white', 'yellow', 'green', 'white', 'white', 'yellow', 'white', 'white', 'green', 
               'white', 'yellow', 'white', 'white', 'white', 'green', 'white', 'yellow', 'white', 'green']
    
    pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 2), (1, 4), (2, 0), (2, 1), (2, 2), 
           (2, 3), (2, 4), (3, 0), (3, 2), (3, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

    words = []
    with open('five_letter_words.txt') as flw:
        for line in flw:
            words.extend(line.split())

    tiles = []
    for count, letter in enumerate(letters):
        tiles.append(Tile(letter, colours[count], pos[count]))
        
    board = Board(size)
    board.add_tiles(tiles)
    solver = Solver(board, words)
    
    result = solver.solve()
    print(result)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
    test_archive_37()