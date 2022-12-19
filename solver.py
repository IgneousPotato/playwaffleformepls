import re
import string
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


    def form_CSP(self):
        temp_board = self.board
        temp_mask = self.mask
        wrong_letters_mask = ''
        
        full_alpha = list(string.ascii_uppercase)
        wrong_letters = set(full_alpha).difference(set(self.letters))
        for letter in wrong_letters:
            if wrong_letters_mask == '':
                wrong_letters_mask += f'{letter}'
            else:
                wrong_letters_mask += f'|{letter}'
                
        domains = {}

        for i in range(2):
            for j in range(int((self.size + 1) / 2)):
                if i == 0:
                    word = temp_board[j*2, :]
                    mask = temp_mask[j*2, :]
                else:
                    word = temp_board[:, j*2]
                    mask = temp_mask[:, j*2]

                domains[i*3 + j] = self.get_domain(word, mask, wrong_letters_mask)
        

    def get_domain(self, word, mask, wrong_letters_mask):
        '''
        Could add a lot more constraints on creating domains and further reduce its size but I cba.
        It works, not the best solution but that's not my goal right now anyway :)
        '''

        g_letters = ''
        y_letters = ''
        y_idx = []
        empty_idx = []

        for count, char in enumerate(mask):
            if char == 1:
                g_letters += word[count]
                y_letters += '.'  
            elif char == 0:
                g_letters += '.'
                y_letters += word[count]
                y_idx.append(count)
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
        
        pattern = re.compile(wrong_letters_mask, re.IGNORECASE)
        word_domain = [x for x in word_domain if not re.search(pattern, x)]

        return word_domain


    def get_constraints(self):
        # TODO FORM CONSTRAINTS BASED ON SIZEEEEEEE 
        # Basically, the elements where row/column intersect have to be the same letter. wow so amazing. wow wow wew
        # fuck it hardcoded for size 5 rn
        constraints = {
            ('0', '3'): lambda word0, word3: word0[0] == word3[0],
            ('3', '0'): lambda word3, word0: word3[0] == word0[0],
            ('0', '4'): lambda word0, word4: word0[2] == word4[0],
            ('4', '0'): lambda word4, word0: word4[0] == word0[2],
            ('0', '5'): lambda word0, word5: word0[4] == word5[0],
            ('5', '0'): lambda word5, word0: word5[0] == word0[4],
            # make it a
            ('1', '3'): lambda word1, word3: word1[0] == word3[2],
            ('3', '1'): lambda word3, word1: word3[2] == word1[0],
            ('1', '4'): lambda word1, word4: word1[2] == word4[2],
            ('4', '1'): lambda word4, word1: word4[2] == word1[2],
            ('1', '5'): lambda word1, word5: word1[4] == word5[2],
            ('5', '1'): lambda word5, word1: word5[2] == word1[4],
            # bit readable
            ('2', '3'): lambda word2, word3: word2[0] == word3[4],
            ('3', '2'): lambda word3, word2: word3[4] == word2[0],
            ('2', '4'): lambda word2, word4: word2[2] == word4[4],
            ('4', '2'): lambda word4, word2: word4[4] == word2[2],
            ('2', '5'): lambda word2, word5: word2[4] == word5[4],
            ('5', '2'): lambda word5, word2: word5[4] == word2[4],
        }
        return constraints


    def get_arcs(self):
        # Also hard coded for now cause fuck it. 
        arcs = [('0', '3'), ('3', '0'), ('0', '4'), ('4', '0'), ('0', '5'), ('5', '0'), 
                ('1', '3'), ('3', '1'), ('1', '4'), ('4', '1'), ('1', '5'), ('5', '1'),
                ('2', '3'), ('3', '2'), ('2', '4'), ('4', '2'), ('2', '5'), ('5', '2')]
        return arcs
