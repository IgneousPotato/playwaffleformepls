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

                poss_word_dict[i*3 + j] = self.poss_words(word, mask, letters)

        # print(poss_word_dict)
        # orderedDict = sorted(poss_word_dict.items(), key=lambda e: e[1][0])
        # print(orderedDict)

        # logging.info("Possible words dictionary")
        # for i in orderedDict:
        #     print(i)
            

    def poss_words(self, word, mask, letters):
        """
        I HATE THIS - I NEED TO REDO THIS LATER. IT WAS BRAIN THOUGHT VOMIT, OKAY? 
        I JUST NEEDED IT TO WORK FIRST. IMPROVEMENTS CAN COME LATER.
        THANKS. BYE.
        """

        r_l = letters
        g_letters = ''
        y_letters = ''
        score = 0

        for count, char in enumerate(mask):
            if char == 1:
                g_letters += word[count]
                y_letters += '.'            
                score += 5
            elif char == 0:
                g_letters += '.'
                y_letters += word[count]
                if count % 2 == 0:
                    score += 1
                else:
                    score += 3
            else:
                g_letters += '.'
                y_letters += '.'

        pattern = re.compile(g_letters, re.IGNORECASE)
        g_mask_domain = [x for x in self.english_words if re.match(pattern, x)]

        logging.info(f'G Mask: {g_letters}')
        print('G Domain:')
        print(f'{g_mask_domain}\n')
        
        if y_letters != '.....':
            y_odd_domain = []
            y_even_domain = []

            ymd = g_mask_domain

            for count, char in enumerate(y_letters): 
                yeven = ymd

                if char != '.':
                    if count % 2 == 0:
                        y_mask_domain = yeven
                    else: 
                        y_mask_domain = ymd

                    # Get mask for single yellow char
                    y_list = list('....')
                    y_list.insert(count, char)
                    y_mask = ''.join(y_list)
                    
                    pattern = re.compile(char, re.IGNORECASE)
                    y_mask_domain = [x for x in y_mask_domain if re.search(pattern, x)]

                    pattern = re.compile(y_mask, re.IGNORECASE)           
                    y_mask_domain = [x for x in y_mask_domain if not re.match(pattern, x)]

                    if g_letters != '.....':
                        for g_count, g_char in enumerate(g_letters):
                            new_y_list = list('....')

                            if g_char != '.' and g_char != char:
                                new_y_list.insert(g_count, char)
                                new_y_mask = ''.join(new_y_list)

                                pattern = re.compile(new_y_mask, re.IGNORECASE)           
                                y_mask_domain = [x for x in y_mask_domain if not re.match(pattern, x)]

                    if count % 2 == 0:
                        yeven = y_mask_domain
                        # y_even_domain.append(y_mask_domain)
                    else:
                        ymd = y_mask_domain
                        # y_odd_domain.append(y_mask_domain)

            '''print(y_odd_domain)
            word_domain = list(set.intersection(*map(set, [y_odd_domain])))
            if word_domain != []:
                word_domain_ext = list(set.intersection(*map(set, [word_domain, y_even_domain])))
            else:
                print(y_even_domain)
                word_domain_ext = list(set.intersection([y_even_domain]))'''
            word_domain = ymd
            word_domain_ext = yeven
        else:
            logging.info('No Y mask\n')
            word_domain = g_mask_domain
            word_domain_ext = g_mask_domain
        
        logging.info(f'Green Letters: {list(g_letters)}')
        logging.info(f'Yellow Letters: {list(y_letters)}')
        logging.info(f'Score: {score}\n')

        logging.info(f'Word Domain: ')
        print(f'{word_domain}\n')

        logging.info(f'Word Domain Extended: ')
        print(f'{word_domain_ext}\n')

        print('\n===============================================================================================================================================')
        print('===============================================================================================================================================\n')

        return word_domain, word_domain_ext