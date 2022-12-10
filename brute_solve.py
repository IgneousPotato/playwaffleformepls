import numpy as np

class BruteSolver:
    letters: list
    words: np.chararray
    
    def __init__(self, board) -> None:
        self.letters = list(tile.letter for tile in board.tiles)
        self.word_matrix = np.empty([5,5], dtype=str)
        for tile in board.tiles:
            self.words[tile.pos] = tile.letter
            
#        self.word1 = board.tiles[0:5]
 #       self.word2 = board.tiles[8:13]
  #      self.word3 = board.tiles[16:21]
   #     self.word4 = board.tiles[0:5]
    #    self.word5 = board.tiles[0:5]
     #   self.word6 = board.tiles[0:5]
        pass
