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
        self.rowcolcount = int((self.size + 1) / 2)
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
        self._arcs, self._constraints = self.get_arcs_constraints()

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
            for j in range(self.rowcolcount):
                if i == 0:
                    word = self.board[j*2, :]
                    mask = self.mask[j*2, :]
                else:
                    word = self.board[:, j*2]
                    mask = self.mask[:, j*2]
                domains[i*self.rowcolcount + j] = self.get_word_domain(word, mask, wrong_letters_mask)
        
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

        if g_letters != '.'*self.size:
            pattern = re.compile(g_letters, re.IGNORECASE)
            g_mask_domain = [x for x in self.words_list if re.match(pattern, x)]
        else:
            g_mask_domain = self.words_list
        
        word_domain = []
        if y_letters[1::2] != '.'*(self.rowcolcount - 1): 
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

    def get_arcs_constraints(self) -> list:
        arcs = []
        constraints = {}

        for i in range(self.rowcolcount):
            for j in range(self.rowcolcount):
                arcs.append((i, j + self.rowcolcount))
                arcs.append((j + self.rowcolcount, i))

                constraints[(i, j + self.rowcolcount)] = self.lambda_constraint(j*2, i*2)
                constraints[(j + self.rowcolcount, i)] = self.lambda_constraint(i*2, j*2)
        
        return arcs, constraints
    
    def lambda_constraint(self, i: int, j: int):
        return lambda wordi, wordj: wordi[i] == wordj[j] 

    def run_AC3(self, domains: dict) -> dict:
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
        self._domains = self.backtrack_search(self._domains)
        dict(sorted(self._domains.items(), key=lambda item: len(item[1])))
        return self._domains

    def find_moves(self) -> list:
        pass
