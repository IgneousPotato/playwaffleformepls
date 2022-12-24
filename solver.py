import re
import copy
import queue
import string
import logging

import numpy as np

from typing import Callable

class Solver:
    board_matrix: np.ndarray
    words_list: set
    
    _arcs: list
    _domains: dict
    _constraints: dict
    
    def __init__(self, board: object, words: list) -> None:
        self.words_list = words

        self.size = board.size
        self.rowcolcount = int((self.size + 1) / 2)

        self.board = board
        self.board_matrix = np.ndarray((self.size, self.size), dtype=list)
        self.mask = np.ndarray((self.size, self.size), dtype=list)

        self.initial_letters = []
        self.solved_letters = []

        for i, tile in enumerate(board.tiles):
            self.board_matrix[board.tile_pos[i]] = tile.letter
            self.initial_letters.append(tile.letter)

            if tile.colour == "green":
                self.mask[board.tile_pos[i]] = 1
            elif tile.colour == "yellow":
                self.mask[board.tile_pos[i]] = 0

        self.idx_unsolved_ltr_map = {}
        self.word_idx_map = {}
        
        self._domains, self.mask_map = self.get_domains_mask_map()
        self._arcs, self._constraints = self.get_arcs_constraints()

    def get_domains_mask_map(self) -> dict | dict:
        wrong_letters_mask = ''
        full_alpha = list(string.ascii_uppercase)
        wrong_letters = set(full_alpha).difference(set(self.initial_letters))
        
        for letter in wrong_letters:
            if wrong_letters_mask == '':
                wrong_letters_mask += f'{letter}'
            else:
                wrong_letters_mask += f'|{letter}'
        
        mask_map = {}
        domains = {}
        for i in range(2):
            for j in range(self.rowcolcount):
                if i == 0:
                    word = self.board_matrix[j*2, :]
                    mask = self.mask[j*2, :]
                else:
                    word = self.board_matrix[:, j*2]
                    mask = self.mask[:, j*2]
                mask_map[i*self.rowcolcount + j] = mask
                domains[i*self.rowcolcount + j] = self.get_word_domain(word, mask, wrong_letters_mask)

        return domains, mask_map

    def get_word_domain(self, word: list, mask: list, wrong_letters_mask: str) -> list:
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

    def get_arcs_constraints(self) -> list | dict:
        arcs = []
        constraints = {}

        for i in range(self.rowcolcount):
            for j in range(self.rowcolcount):
                arcs.append((i, j + self.rowcolcount))
                arcs.append((j + self.rowcolcount, i))

                constraints[(i, j + self.rowcolcount)] = self.lambda_constraint(j*2, i*2)
                constraints[(j + self.rowcolcount, i)] = self.lambda_constraint(i*2, j*2)
        
        return arcs, constraints
    
    def lambda_constraint(self, i: int, j: int) -> Callable:
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

    def check_letters(self, domain: dict) -> bool:
        letters_string = ''

        for key in domain:
            if key <= (self.size - 1) / 2:
                letters_string += domain[key][0].upper()
            else:
                letters_string += domain[key][0][1::2].upper()
                
        return sorted(list(letters_string)) == sorted(self.initial_letters)

    def get_solved_letters(self) -> list:
        if all(len(value) != 1 for value in self._domains.values()):
            logging.error('Domain is not yet solved.')
            return None

        solved_board = []

        size = int((len(self._domains) + 1) / 2 )
        for i in range(size):
            solved_board.extend(list(self._domains[i][0]))
            
            if i == size - 1:
                break

            for j in range(size):
                solved_board.append(self._domains[j+size][0][i*2+1])

        return list(map(lambda x: x.upper(), solved_board))
        
    def solve(self) -> dict:
        self.run_AC3(self._domains)
        self._domains = self.backtrack_search(self._domains)

        if self._domains != None:
            dict(sorted(self._domains.items(), key=lambda item: len(item[1])))

        return self._domains
    
    def find_best_moves(self) -> list:
        self.solved_letters = self.get_solved_letters()
        self.idx_unsolved_ltr_map, self.word_idx_map = self.get_idx_word_rels()
        
        best_moves = self.greedy_search(self.initial_letters, [], 0, self.idx_unsolved_ltr_map)
        return best_moves
         
    def greedy_search(self, state: list, moves_list: list, depth: int, idx_unslvd_ltrs: dict):
        if self.size == 5:
            max_depth = 10
        elif self.size == 7:
            max_depth = 20

        if depth == max_depth and state == self.solved_letters:
            return moves_list
        elif depth == max_depth and state != self.solved_letters: 
            return None

        cur_state_moves = self.possible_moves(state)
        for move in cur_state_moves:
            moves_list.append((move[0], move[1], state[move[0]], state[move[1]]))
            new_idx_unslvd_ltrs = self.update_unsolved_ltrs(move, state, idx_unslvd_ltrs)
            new_state = self.update_state(move, state)

            result = self.greedy_search(new_state, moves_list, depth + 1, new_idx_unslvd_ltrs)

            if result == None:
                del moves_list[-1]
            else: 
                return moves_list

        return None

    def get_idx_word_rels(self):
        idx_word_map = {}
        count = 0

        for i in range(self.rowcolcount):
            for j in range(self.size):
                word_keys = [i]
                word_ltrs = [[x for y, x in enumerate(self._domains[i][0].upper()) if self.mask_map[i][y] != 1]]
                idx_word_map[count] = [word_keys, word_ltrs]
                
                count += 1
                        
            for j in range(self.rowcolcount):                
                word_keys = [j + self.rowcolcount]
                word_ltrs = [x for y, x in enumerate(self._domains[j + self.rowcolcount][0].upper()) if self.mask_map[j + self.rowcolcount][y] != 1]
                
                if i != self.rowcolcount - 1:
                    idx_word_map[count] = [word_keys, word_ltrs]

                idx_word_map[count - (self.size - j)][0].extend(word_keys)
                idx_word_map[count - (self.size - j)][1].append(word_ltrs)
                
                count += 1

        word_idx_map = {}
        for k, v in idx_word_map.items():
            for i in v[0]:
                if i not in word_idx_map:
                    word_idx_map[i] = [k]
                else:
                    word_idx_map[i].append(k)
        
        return idx_word_map, word_idx_map

    def update_unsolved_ltrs(self, move: tuple, state: list, idx_unsolved_ltr_map: dict) -> dict:
        map_copy = copy.deepcopy(idx_unsolved_ltr_map)

        if state[move[0]] == self.solved_letters[move[1]]: # if True, it becomes a greent tile
            for idxs in self.word_idx_map.values():
                if move[1] in idxs: # find words that contain the index its moving to
                    for idx in idxs: # loop through each word
                        ltrs = map_copy[idx][1] # check if tile moved is in the list of unsolved letters
                        if state[move[0]] in ltrs:
                            ltrs.remove(state[move[0]])

        if state[move[1]] == self.solved_letters[move[0]]:
            for idxs in self.word_idx_map.values():
                if move[0] in idxs:
                    for idx in idxs:
                       ltrs = map_copy[idx][1]
                       if state[move[1]] in ltrs:
                            ltrs.remove(state[move[1]])
        return map_copy
    
    def update_state(self, move: tuple, state: list) -> list:
        copy_state = list(state)

        lt1 = copy_state[move[0]]
        lt2 = copy_state[move[1]]

        copy_state[move[1]] = lt1
        copy_state[move[0]] = lt2

        return copy_state
 
    def eval_letter(self, idx: int, letter: str) -> int:
        if letter == self.solved_letters[idx]:
            return 5
        else:
            idx_words = self.idx_unsolved_ltr_map[idx][1]
            for word in idx_words:
                if letter in word:
                    return 2
        return 0

    def possible_moves(self, state: list) -> list:
        poss_moves = []
        for idx1, lt1 in enumerate(state):
            if lt1 != self.solved_letters[idx1]:
                for idx2, lt2 in enumerate(state):
                    if lt1 != lt2 and lt2 != self.solved_letters[idx2]:
                        cost = self.eval_letter(idx1, lt2) + self.eval_letter(idx2, lt1)
                        move = (idx1, idx2, cost)
                        if cost > 4:
                            poss_moves.append(move)
        
        poss_moves.sort(key=lambda x: x[2], reverse=True)
        return poss_moves
