import re
import queue
import string
import logging

from typing import Callable

import numpy as np


class Solver:
    board_matrix: np.ndarray
    words_list: set
    initial_letters: list

    def __init__(self, board: object, words: list) -> None:
        self.words_list = words

        self.size = board.size
        self.rowcolcount = int((self.size + 1) / 2)

        self.board = board
        self.board_matrix = np.ndarray((self.size, self.size), dtype=list)
        self.mask = np.ndarray((self.size, self.size), dtype=list)

        self.initial_letters = []

        for i, tile in enumerate(board.tiles):
            self.board_matrix[board.tile_pos[i]] = tile.letter
            self.initial_letters.append(tile.letter)

            match tile.colour:
                case "green":
                    self.mask[board.tile_pos[i]] = 1
                case "yellow":
                    self.mask[board.tile_pos[i]] = 0

        self._domains = self.get_domains()
        self._arcs, self._constraints = self.get_arcs_constraints()
        self.poss_solutions = {}

        self.next_node_dict = {}
        self.largest_cycle = 0
        self.certain_cycles = []

    def get_initial_state(self) -> list:
        return self.initial_letters

    def get_domains(self) -> dict | dict:
        wrong_letters_mask = ''
        full_alpha = list(string.ascii_uppercase)
        wrong_letters = set(full_alpha).difference(set(self.initial_letters))

        for letter in wrong_letters:
            if wrong_letters_mask == '':
                wrong_letters_mask += f'{letter}'
            else:
                wrong_letters_mask += f'|{letter}'

        domains = {}
        for i in range(2):
            for j in range(self.rowcolcount):
                if i == 0:
                    word = self.board_matrix[j*2, :]
                    mask = self.mask[j*2, :]
                else:
                    word = self.board_matrix[:, j*2]
                    mask = self.mask[:, j*2]

                domains[i*self.rowcolcount +
                        j] = self.get_word_domain(word, mask, wrong_letters_mask)

        return domains

    def get_word_domain(self, word: list, mask: list, wrong_letters_mask: str) -> list:
        g_letters = ''
        y_letters = ''
        y_idx = []
        empty_idx = []

        for count, char in enumerate(mask):
            match char:
                case 1:
                    g_letters += word[count]
                    y_letters += '.'
                case 0:
                    g_letters += '.'
                    y_letters += word[count]
                    y_idx.append(count)
                case _:
                    g_letters += '.'
                    y_letters += '.'
                    empty_idx.append(count)

        if g_letters != '.'*self.size:
            pattern = re.compile(g_letters, re.IGNORECASE)
            g_mask_domain = [
                x for x in self.words_list if re.match(pattern, x)]
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
                    words_with_y = [
                        x for x in g_mask_domain if re.search(pattern, x)]

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

                constraints[(i, j + self.rowcolcount)
                            ] = self.lambda_constraint(j*2, i*2)
                constraints[(j + self.rowcolcount, i)
                            ] = self.lambda_constraint(i*2, j*2)

        return arcs, constraints

    def lambda_constraint(self, i: int, j: int) -> Callable:
        return lambda wordi, wordj: wordi[i] == wordj[j]

    def run_AC3(self, domains: dict) -> dict:
        arc_list = queue.Queue()
        for arc in self._arcs:
            arc_list.put(arc)

        while not arc_list.empty():
            (x_i, x_j) = arc_list.get()

            if len(domains[x_i]) == 0:
                return None

            if self._remove_inconsistent_values(x_i, x_j, domains):
                xi_neighbours = [
                    neighbour for neighbour in self._arcs if neighbour[0] == x_i]

                for neighbour in xi_neighbours:
                    arc_list.put(neighbour)

        return domains

    def _remove_inconsistent_values(self, x_i: object, x_j: object, domains: dict) -> bool:
        removed = False
        xi_domain = domains[x_i]
        xj_domain = domains[x_j]

        for x in xi_domain:
            satisfy = False

            cons = [con for con in self._constraints if con[0]
                    == x_i and con[1] == x_j]

            for y in xj_domain:
                for constraint in cons:
                    f_con = self._constraints[constraint]

                    if f_con(x, y):
                        satisfy = True

            if not satisfy:
                xi_domain.remove(x)
                removed = True

        return removed

    def backtrack_search(self, running_dom: dict, print_: bool = False) -> dict:
        if print_:
            print()
            logging.info('Testing domain: %s', running_dom)

            stack = []
            for values in running_dom.values():
                if len(values) == 1:
                    stack.append(values[0])
                if len(values) > 1:
                    break
            logging.info('Current Stack 2: %s', " -> ".join(stack))

        if all(len(value) == 1 for value in running_dom.values()) and self.check_valid_sol(running_dom):
            if running_dom not in [x for x in self.poss_solutions.values()]:
                if print_:
                    logging.info('FOUND NEW VALID SOLUTION!!!!!!!!!!!!!!!!!')
                    logging.info('SOLUTION: %s', running_dom)
                self.poss_solutions[len(self.poss_solutions)] = running_dom
            return None

        for key, values in running_dom.items():
            if len(values) > 1:
                break
        else:
            return None

        for value in values:
            new_domains = {k: v[:] for k, v in running_dom.items()}
            new_domains[key] = [value]

            if self.run_AC3(new_domains) is None:
                continue

            result = self.backtrack_search(new_domains, print_)
            if result is not None:
                return result

        return None

    def check_valid_sol(self, domain: dict) -> bool:
        letters_string = ''

        for key in domain:
            if key <= (self.size - 1) / 2:
                letters_string += domain[key][0].upper()
            else:
                letters_string += domain[key][0][1::2].upper()

        return sorted(list(letters_string)) == sorted(self.initial_letters)

    def get_solved_letters(self, domains) -> list:
        if all(len(value) != 1 for value in domains.values()):
            logging.error('Domain is not yet solved.')
            return None

        solved_board = []

        size = int((len(domains) + 1) / 2)
        for i in range(size):
            solved_board.extend(list(domains[i][0]))

            if i == size - 1:
                break

            for j in range(size):
                solved_board.append(domains[j + size][0][i * 2 + 1])

        return list(map(lambda x: x.upper(), solved_board))

    def solve(self) -> dict:
        self.run_AC3(self._domains)
        self._domains = dict(sorted(self._domains.items(),
                             key=lambda item: len(item[1])))
        self.backtrack_search(self._domains)
        for domain in self.poss_solutions.values():
            if domain is not None:
                domain = dict(
                    sorted(domain.items(), key=lambda item: len(item[1])))

        if not self.poss_solutions:
            return None

        return self.poss_solutions

    def find_best_moves(self, solved_puzzle: str | dict) -> list:
        self.next_node_dict = {}
        self.certain_cycles = []

        match solved_puzzle:
            case dict():
                solved_letters = self.get_solved_letters(solved_puzzle)
            case str():
                solved_letters = list(solved_puzzle)
            case _:
                logging.error(
                    'find_best_moves() cannot parse given solution type. Only accepts str or dict.')

        for path, lt in enumerate(self.initial_letters):
            self.form_next_node_dict(
                self.initial_letters, lt, path, solved_letters)

        self.next_node_dict = dict(
            sorted(self.next_node_dict.items(), key=lambda item: len(item[1])))

        self.find_cyclic_paths()
        best_moves = self.form_moves_from_cycles(solved_letters)

        return best_moves

    def form_next_node_dict(self, state: list, letter: str, pos: int, solved_letters: list) -> None:
        if letter == solved_letters[pos]:
            return

        self.next_node_dict[pos] = []

        for idx, ltr in enumerate(state):
            if idx == pos or ltr == solved_letters[idx]:
                continue
            if letter == solved_letters[idx]:
                self.next_node_dict[pos].append(idx)

    def find_cyclic_paths(self) -> None:
        uncertain_cycles = []
        # next time is specific to wafflegame.net to reach in 10 or 20 (for deluxe) move
        # dont know how it'd work for non-wafflegame.net puzzles that may need more than
        # that to be solved. I also don't care.
        # otherwise setting the value to len(self.next_node_dict) should work. maybe. idc.
        self.largest_cycle = 22 - len(self.next_node_dict)
        num_req_cycles = len(self.next_node_dict) - 10

        if self.size == 7:
            self.largest_cycle += 20
            num_req_cycles += 10

        for k in self.next_node_dict:
            if not any(k in path for path in self.certain_cycles):
                for path in self.find_elem_cyclic_path(k, k, [k]):
                    if path is None:
                        continue

                    path_set = set(path)
                    if len(path) == 2:
                        self.certain_cycles.append(list(path_set))
                        break

                    if path_set not in uncertain_cycles:
                        uncertain_cycles.append(path_set)
                    else:
                        continue

        if len(self.certain_cycles) == num_req_cycles:
            pass
        else:
            valid_uncertain_cycles = []

            for u_path in uncertain_cycles:
                if not any(bool(set(c_path) & u_path) for c_path in self.certain_cycles):
                    valid_uncertain_cycles.append(u_path)
                    continue

            if num_req_cycles - len(self.certain_cycles) == len(valid_uncertain_cycles):
                for cycle in valid_uncertain_cycles:
                    self.certain_cycles.append(list(cycle))
                return

            valid_uncertain_cycles = sorted(valid_uncertain_cycles, key=len)

            buffer_cycles = []
            node_track = []

            for cyc in valid_uncertain_cycles:
                if not buffer_cycles:
                    buffer_cycles.append(cyc)
                    node_track.extend(x for x in cyc)
                    continue

                if not any(node in node_track for node in cyc):
                    buffer_cycles.append(cyc)
                    node_track.extend(x for x in cyc)

            for b_cyc in buffer_cycles:
                self.certain_cycles.append(list(b_cyc))

    def find_elem_cyclic_path(self, pos: int, goal_pos: int, cur_path: list) -> list:
        if goal_pos in self.next_node_dict[pos]:
            yield cur_path[:]
        else:
            if len(cur_path) >= self.largest_cycle:
                yield None

            for running_pos in self.next_node_dict[pos]:
                if any(running_pos in path for path in self.certain_cycles):
                    continue

                if running_pos in cur_path:
                    continue

                cur_path.append(running_pos)
                for path in self.find_elem_cyclic_path(running_pos, goal_pos, cur_path):
                    if path is not None:
                        if len(path) <= self.largest_cycle:
                            yield path
                        else:
                            yield None

                cur_path.remove(running_pos)

    def set_common_paths(self, shortest_path: list) -> None:
        working_path = shortest_path[:-1]
        elem = working_path[-1]

        if elem in self.certain_cycles:
            return

        working_path.insert(0, elem)
        self.certain_cycles[elem] = working_path
        self.set_common_paths(working_path)

    def eval_green(self, idx: int, letter: str, solved_letters: list) -> bool:
        if letter == solved_letters[idx]:
            return True

    def swap(self, idx1: int, idx2: int, state: list) -> list:
        temp1 = state[idx1]

        state[idx1] = state[idx2]
        state[idx2] = temp1

        return state

    def form_moves_from_cycles(self, solved_letters: list) -> list:
        moves = []
        working_state = self.initial_letters[:]

        for cyclic_path in self.certain_cycles:
            working_cycle = cyclic_path[:]

            i = 0
            while i < len(working_cycle):
                idx1 = working_cycle[i]
                for idx2 in working_cycle:
                    if idx1 != idx2:
                        check1 = self.eval_green(
                            idx1, working_state[idx2], solved_letters)
                        if check1:
                            moves.append(
                                (idx1, idx2, working_state[idx1], working_state[idx2]))

                            working_state = self.swap(
                                idx1, idx2, working_state)
                            working_cycle.remove(idx1)

                            i = 0
                            break
                i += 1
        return moves
