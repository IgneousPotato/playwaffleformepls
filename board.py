import numpy as np

class Board:
    board_matrix: np.matrix
    index_matrix: np.matrix
    letters_colour: dict

    def __init__(self) -> None:
        self.board_matrix = np.zeros([5, 5], dtype=int)
        self.index_matrix = np.matrix('22 23 24 25 26; 27 0 28 0 29; 30 31 32 33 34; 35 0 36 0 37; 38 39 40 41 42')
        print(self.index_matrix)
        self.letters_colour = {}

    def add_elements(self, elements: dict) -> None:
        for key in elements:
            element = elements[key]
            self.board_matrix[element[-1], element[-2]] = key
            self.index_matrix[element[-1], element[-2]] = key + 21
            self.letters_colour[key] = [element[0], element[1]]
        
    def view_board(self) -> None:
        print(self.board_matrix)

    def view_letter_status(self) -> None:
        print(self.letters_colour)
