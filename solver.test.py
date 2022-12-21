import unittest

from tile import Tile
from board import Board
from solver import Solver

class TestBoardSolver(unittest.TestCase):
    def test_archive_1(self):
        size = 5
        
        letters = ['F', 'B', 'O', 'U', 'E',
                 'G', 'I', 'U',
                 'L', 'S', 'O', 'O', 'M',
                 'G', 'E', 'L',
                 'O', 'E', 'M', 'N', 'A']
        
        colours = ['green', 'white', 'white', 'green', 'green',
                   'white', 'white', 'white',
                   'green', 'yellow', 'green', 'yellow', 'yellow',
                   'white', 'yellow', 'white',
                   'green', 'yellow', 'yellow', 'white', 'green']
        
        pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
               (1, 0), (1, 2), (1, 4), 
               (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), 
               (3, 0), (3, 2), (3, 4), 
               (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

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

        exp_solution = {0: ['fugue'], 1: ['loose'], 2: ['omega'], 3: ['folio'], 4: ['globe'], 5:['enema']}
        result = solver.solve()

        self.assertEqual(exp_solution, result)
    
    def test_archive_37(self):
        size = 5
        
        letters = ['Q', 'T', 'G', 'U', 'L',
                 'Y', 'U', 'G',
                 'D', 'U', 'I', 'O', 'E',
                 'T', 'N', 'E',
                 'N', 'E', 'I', 'L', 'Y']
        
        colours = ['green', 'white', 'white', 'yellow', 'green',
                   'white', 'white', 'yellow',
                   'white', 'white', 'green', 'white', 'yellow',
                   'white', 'white', 'white',
                   'green', 'white', 'yellow', 'white', 'green']
        
        pos = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
               (1, 0), (1, 2), (1, 4), 
               (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), 
               (3, 0), (3, 2), (3, 4), 
               (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]

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
        
        exp_solution = { 0: ['quill'], 1: ['eying'], 2: ['nutty'], 3: ['queen'], 4: ['idiot'], 5: ['leggy']}
        result = solver.solve()

        self.assertEqual(exp_solution, result)

if __name__ == "__main__":
    unittest.main()
