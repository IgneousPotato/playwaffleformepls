import unittest

from board import Board
from solver import Solver
from run_manual import parse_letters, parse_colours, get_pos, get_words, load_tiles, run

class TestBoardSolver(unittest.TestCase):
    def test_archive_1(self):
        size = 5
        
        letters = parse_letters('FBOUEGIULSOOMGELOEMNA')
        colours = parse_colours('gwwggwwwgygyywywgyywg')

        pos = get_pos(size)
        words = get_words(size)
            
        board = Board(size)
        board.add_tiles(load_tiles(letters, colours, pos))
        solver = Solver(board, words)

        exp_solution = {0: ['fugue'], 1: ['loose'], 2: ['omega'], 3: ['folio'], 4: ['globe'], 5:['enema']}
        result = solver.solve()

        self.assertEqual(exp_solution, result)
    
    def test_archive_37(self):
        size = 5
        
        letters = parse_letters('QTGULYUGDUIOETNENEILY')
        colours = parse_colours('gwwygwwywwgwywwwgwywg')

        pos = get_pos(size)
        words = get_words(size)
            
        board = Board(size)
        board.add_tiles(load_tiles(letters, colours, pos))
        solver = Solver(board, words)
        
        exp_solution = {0: ['quill'], 1: ['eying'], 2: ['nutty'], 3: ['queen'], 4: ['idiot'], 5: ['leggy']}
        result = solver.solve()

        self.assertEqual(exp_solution, result)

    def test_deluxe_30(self):
        size = 7

        letters = parse_letters('MLLNPOELYGYIBPLIADEOEOAEETTLRNEARAIDSRRC')
        colours = parse_colours('wwgwgyywwwygwgggwgywyygwgggwgywyywwgwgww')

        pos = get_pos(size)
        words = get_words(size)
            
        board = Board(size)
        board.add_tiles(load_tiles(letters, colours, pos))
        solver = Solver(board, words)
        
        exp_solution = {0: ['calypso'], 1: ['implied'], 2: ['abettor'], 3: ['elderly'], 4: ['coinage'], 5: ['lipread'], 6: ['painter'], 7: ['orderly']}
        result = solver.solve()

        self.assertEqual(exp_solution, result)

if __name__ == "__main__":
    unittest.main()
