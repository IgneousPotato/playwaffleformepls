import re
import logging

import numpy as np

from tile import Tile

class Solver:
    letters: list
    size: int
    board: np.ndarray
    mask: np.ndarray
    y_mask: np.ndarray
    english_words: set
    
    def __init__(self, board, words) -> None:
        self.size = board.size
        self.letters = list(tile.letter for tile in board.tiles)
        self.board = np.ndarray((self.size, self.size), dtype=list)
        self.mask = np.ndarray((self.size, self.size), dtype=list)
        
        for tile in board.tiles:
            self.board[tile.pos] = tile.letter
            if tile.colour == "green":
                self.mask[tile.pos] = 1
            elif tile.colour == "yellow":
                self.mask[tile.pos] = 0

        self.english_words = words

    def brute_force(self):
        temp_board = self.board
        temp_mask = self.mask
        
        letters = self.letters

        for i in range(2):
            for j in range(int((self.size + 1) / 2)):
                if i == 0:
                    word = temp_board[j*2, :]
                    mask = temp_mask[j*2, :]
                else:
                    word = temp_board[:, j*2]
                    mask = temp_mask[:, j*2]

                self.poss_words(word, mask, letters)
            
    def poss_words(self, word, mask, letters):
        r_l = letters
        g_w = ''
        y_w = ''

        for count, letter in enumerate(mask):
            if letter == 1:
                g_w += word[count]
                y_w += '.'
            elif letter == 0:
                g_w += '.'
                y_w += word[count]
            else:
                g_w += '.'
                y_w += '.'

        pattern = re.compile(g_w, re.IGNORECASE)
        possible_words = [x for x in self.english_words if re.match(pattern, x)]
        
        horrible_dict = {}
        for count, char in enumerate(y_w):
            if char != '.':
                y_list = list('....')
                y_list.insert(count, char)
                y_mask = ''.join(y_list)

                pattern = re.compile(y_mask, re.IGNORECASE)
                horrible_dict[2*count] = [x for x in possible_words if not re.match(pattern, x)]

                pattern = re.compile(char, re.IGNORECASE)
                horrible_dict[2*count+1] = [x for x in horrible_dict[2*count] if re.search(pattern, x)]
        
        dict_list_main = list(horrible_dict.values())[::2]
        dict_list = list(horrible_dict.values())
        possible_words = list(set.intersection(*map(set, dict_list_main)))
        possible_words_ext = list(set.intersection(*map(set, dict_list)))
        
        logging.info(f"Green Letters: {g_w}")
        logging.info(f"Yellow Letters: {y_w}")
        logging.info(f"Possible Words:")
        print(possible_words)
        logging.info(f"Possible Words Extended:")
        print(possible_words_ext)
        print()