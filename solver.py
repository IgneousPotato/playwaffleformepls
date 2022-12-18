import re
import logging

import numpy as np

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

        poss_word_dict = {}

        for i in range(2):
            for j in range(int((self.size + 1) / 2)):
                if i == 0:
                    word = temp_board[j*2, :]
                    mask = temp_mask[j*2, :]
                else:
                    word = temp_board[:, j*2]
                    mask = temp_mask[:, j*2]

                poss_word_dict[i*3 + j] = self.get_domain(word, mask)
            

    def get_domain(self, word, mask):
        g_letters = ''
        y_letters = ''
        y_idx = []
        empty_idx = []
        score = 0

        for count, char in enumerate(mask):
            if char == 1:
                g_letters += word[count]
                y_letters += '.'            
                score += 5
            elif char == 0:
                g_letters += '.'
                y_letters += word[count]
                y_idx.append(count)
                if count % 2 == 0:
                    score += 1
                else:
                    score += 3
            else:
                g_letters += '.'
                y_letters += '.'
                empty_idx.append(count)

        if g_letters != '.....':
            pattern = re.compile(g_letters, re.IGNORECASE)
            g_mask_domain = [x for x in self.english_words if re.match(pattern, x)]
        else:
            g_mask_domain = self.english_words
            
        word_domain = []
        if y_letters[1::2] != '..': 
            count = 1

            while count < self.size: 
                current_char = y_letters[count].lower()
                
                if current_char != '.':            
                    temp_y_idx = y_idx
                    temp_y_idx.remove(count)
                    y_mask = empty_idx + temp_y_idx

                    pattern = re.compile(current_char, re.IGNORECASE)
                    words_with_y = [x for x in g_mask_domain if re.search(pattern, x)]

                    for word in words_with_y:
                        if current_char in [word[i] for i in y_mask]:
                            word_domain.append(word) 
                count += 2
        else:
            word_domain = g_mask_domain

        print()
        logging.info(f'Green Letters: {list(g_letters)}')
        logging.info(f'Yellow Letters: {list(y_letters)}')
        logging.info(f'Score: {score}\n')
        logging.info(f'Word domain:')
        print(word_domain)
        print()

        return word_domain, score
        