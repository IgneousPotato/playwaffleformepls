import re
import queue
import string
import logging

import numpy as np

class Solver:
    board: np.ndarray
    words_list: set
    
    _arcs: list
    _domains: dict
    _constraints: dict
    
    def __init__(self, board: object, words) -> None:
        self.words_list = words
        self.size = board.size
        self.board = np.ndarray((self.size, self.size), dtype=list)
        self.mask = np.ndarray((self.size, self.size), dtype=list)
        self.letters = []

        for tile in board.tiles:
            self.board[tile.pos] = tile.letter
            self.letters.append(tile.letter)

            if tile.colour == "green":
                self.mask[tile.pos] = 1
            elif tile.colour == "yellow":
                self.mask[tile.pos] = 0

        self._domains = self.get_domains()
        self._constraints = self.get_constraints()
        self._arcs = self.get_arcs()

    def get_domains(self) -> dict:
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
                    word = self.board[j*2, :]
                    mask = self.mask[j*2, :]
                else:
                    word = self.board[:, j*2]
                    mask = self.mask[:, j*2]
                domains[i*3 + j] = self.get_word_domain(word, mask, wrong_letters_mask)

        return domains

    def get_word_domain(self, word, mask, wrong_letters_mask) -> list:
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
            g_mask_domain = [x for x in self.words_list if re.match(pattern, x)]
        else:
            g_mask_domain = self.words_list
            
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

    def get_constraints(self) -> dict:
        # TODO FORM CONSTRAINTS BASED ON SIZEEEEEEE 
        # Basically, the elements where row/column intersect have to be the same letter. wow so amazing. wow wow wew
        # fuck it hardcoded for size 5 rn
        # probs make a lambda function generator for it
        constraints = {
            (0, 3): lambda word0, word3: word0[0] == word3[0],
            (3, 0): lambda word3, word0: word3[0] == word0[0],
            (0, 4): lambda word0, word4: word0[2] == word4[0],
            (4, 0): lambda word4, word0: word4[0] == word0[2],
            (0, 5): lambda word0, word5: word0[4] == word5[0],
            (5, 0): lambda word5, word0: word5[0] == word0[4],
            #make it a
            (1, 3): lambda word1, word3: word1[0] == word3[2],
            (3, 1): lambda word3, word1: word3[2] == word1[0],
            (1, 4): lambda word1, word4: word1[2] == word4[2],
            (4, 1): lambda word4, word1: word4[2] == word1[2],
            (1, 5): lambda word1, word5: word1[4] == word5[2],
            (5, 1): lambda word5, word1: word5[2] == word1[4],
            #bit readable
            (2, 3): lambda word2, word3: word2[0] == word3[4],
            (3, 2): lambda word3, word2: word3[4] == word2[0],
            (2, 4): lambda word2, word4: word2[2] == word4[4],
            (4, 2): lambda word4, word2: word4[4] == word2[2],
            (2, 5): lambda word2, word5: word2[4] == word5[4],
            (5, 2): lambda word5, word2: word5[4] == word2[4]
        }
        return constraints

    def get_arcs(self) -> list:
        # Also hard coded for now cause fuck it. 
        arcs = [(0, 3), (3, 0), (0, 4), (4, 0), (0, 5), (5, 0), 
                (1, 3), (3, 1), (1, 4), (4, 1), (1, 5), (5, 1),
                (2, 3), (3, 2), (2, 4), (4, 2), (2, 5), (5, 2)]
        return arcs
    
    def run_AC3(self, domains: dict = None) -> dict:
        if domains == None:
            domains = self._domains

        arc_list = queue.Queue() 
        [arc_list.put(arc) for arc in self._arcs]

        while not arc_list.empty():
            (xi, xj) = arc_list.get()

            if len(domains[xi]) == 0:
                return None

            if self._remove_inconsistent_values(xi, xj, domains):
                xi_neighbours = [neighbour for neighbour in self._arcs if neighbour[0] == xi]

                [arc_list.put(neighbour) for neighbour in xi_neighbours]
        
        return domains
        
    def _remove_inconsistent_values(self, xi: object, xj: object, domains:dict) -> bool:
        removed = False
        xi_domain = domains[xi]
        xj_domain = domains[xj]     
        
        for x in xi_domain:
            satisfy = False

            cons = [con for con in self._constraints if con[0] == xi and con[1] == xj]

            for y in xj_domain:
                for constraint in cons:
                    f_con = self._constraints[constraint]

                    if f_con(x, y):
                        satisfy = True
            
            if not satisfy:
                xi_domain.remove(x)
                removed = True

        return removed

    def backtrack_search(self, domains: dict, print_: bool = False) -> dict:
        if print_:
            print()
            logging.info(f'Testing domain: {domains}')

            stack = []
            for values in domains.values():
                if len(values) == 1:
                    stack.append(values[0])
                if len(values) > 1:
                    break
            logging.info(f'Current Stack 2: {" -> ".join(stack)}')

        if all(len(value) == 1 for value in domains.values()) and self.check_letters(domains):
            logging.info('FOUND VALID SOLUTION!!!!!!!!!!!!!!!!!')
            return domains
        
        for key, values in domains.items():
            if len(values) > 1:
                break
        else:
            return None

        for value in values:
            new_domains = {k: v[:] for k, v in domains.items()}
            new_domains[key] = [value]

            if self.run_AC3(new_domains) == None:
                continue

            result = self.backtrack_search(new_domains, print_)
            if result is not None:
                return result
        return None

    def check_letters(self, dictionary):
        letters_string = ''

        for key in dictionary:
            if key <= (self.size - 1) / 2:
                letters_string += dictionary[key][0].upper()
            else:
                letters_string += dictionary[key][0][1::2].upper()
        
        return sorted(list(letters_string)) == sorted(self.letters)
        
    def solve(self) -> dict:
        self.run_AC3(self._domains)
        self._domains = dict(sorted(self._domains.items(), key=lambda item: len(item[1])))
        return self.backtrack_search(self._domains)
