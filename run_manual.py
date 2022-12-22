#!/usr/bin/env python
import logging

from sys import argv
from typing import Union

from tile import Tile
from board import Board
from solver import Solver

def extract_file(file_name: str) -> Union(int, list, list):
    if file_name.endswith('.txt'):
        with open(file_name) as f:
            size = int(f.readline())
            strings = list(f.readline())
            colours_str = f.readline()
    else:
        logging.error('File type is incorrect. It must be a .txt file.')

    return size, strings, parse_colours(colours_str)

def parse_letters(ltr_str: str) -> list:
    return list(ltr_str)

def parse_colours(col_str: str) -> list:
    colours = []
    for col in col_str:
        if col == 'w':
            colours.append('white')
        elif col == 'g':
            colours.append('green')
        else: 
            colours.append('yellow')
    
    return colours

def get_pos(size: int) -> list:
    pos = []
    for i in range(size):
        for j in range(size):
            if i % 2 != 0 and j % 2 != 0:
                continue 
            else:
                pos.append((i, j))
    
    return pos

def get_words(size: int) -> list:
    if size == 5:
        dict_file = 'five_letter_words.txt'
    elif size == 7:
        dict_file = 'seven_letter_words.txt'
    
    words = []
    # words from https://www.bestwordlist.com/
    with open(dict_file) as flw:
        for line in flw:
            words.extend(line.split())
    
    return words

def load_tiles(letters: list, colours: list, pos: list) -> list:
    tiles = []
    for count, letter in enumerate(letters):
        tiles.append(Tile(letter, colours[count], pos[count]))
    
    return tiles

def run_file_from_code(file_name: str) -> dict:
    # if I want to open a file from another script
    sz, lt, cl = extract_file(file_name)
    return run(sz, lt, cl)

def run(size: int, letters: list, colours: list) -> dict:
    try:
        pos = get_pos(size)
        words = get_words(size)
        
        board = Board(size)
        board.add_tiles(load_tiles(letters, colours, pos))
        BS = Solver(board, words)
        sol = BS.solve()
        return sol
    except:
        logging.error('Something went wrong. Were your inputs valid?')

def main():
    try: 
        print("""                                                                                                 
 _____ _____ _____    _ _ _ _____ _____ _____ __    _____    _____ _____ __    _____ _____ _____ 
|     |   __|  |  |  | | | |  _  |   __|   __|  |  |   __|  |   __|     |  |  |  |  |   __| __  |
| | | |   __|     |  | | | |     |   __|   __|  |__|   __|  |__   |  |  |  |__|  |  |   __|    -|
|_|_|_|_____|__|__|  |_____|__|__|__|  |__|  |_____|_____|  |_____|_____|_____|\___/|_____|__|__|
                                                                                                 
""")
        try:
            sz, lt, cl = extract_file(argv[1])
        except FileNotFoundError:
            logging.error('File not found')
        except IndexError:
            logging.info('No file given. Enter manual input.')
            logging.info('Keyboard interrupt (Ctrl + C) to end.')
            logging.info('P.S. Right click to paste string in terminal :)\n')

            sz = int(input('Enter size: '))
            logging.info(f"Letters string and colours string should be of length {int((sz + 1) * (3*sz - 1) * 0.25)}.")
            lt = parse_letters(input('Enter letters string: '))
            cl = parse_colours(input('Enter colours string: '))
        
        sol = run(sz, lt, cl)
        print(sol)
    except KeyboardInterrupt:
        print()
        logging.info('Keyboard Interrupt')
        logging.info('Exitting')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
    main()