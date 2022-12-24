#!/usr/bin/env python
import logging

from sys import argv

from tile import Tile
from board import Board
from solver import Solver

def extract_file(file_name: str) -> int | list | list:
    if file_name.endswith('.txt'):
        with open(file_name) as f:
            size = int(f.readline().strip('\n'))
            letters = f.readline().strip('\n')
            colours = f.readline()
    else:
        logging.error('File type is incorrect. It must be a .txt file.')
        quit()

    return size, parse_letters(letters), parse_colours(colours)

def parse_letters(ltr_str: str) -> list:
    return list(ltr_str.upper())

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

def load_tiles(letters: list, colours: list) -> list:
    # Only for Board object, not Web_Board object
    tiles = []
    for count, letter in enumerate(letters):
        tiles.append(Tile(letter, colours[count]))
    
    return tiles

def open_file_ext_code(file_name: str):
    # if I want to open a file from another script
    # returns size, letters, colours
    return extract_file(file_name)

def run(size: int, letters: list, colours: list) -> dict | list:
    try:
        words = get_words(size)

        board = Board(size)
        board.add_tiles(load_tiles(letters, colours))
        print(f'{board}')

        BS = Solver(board, words)
        sol = BS.solve()

        if sol == None:
            logging.info('No valid solution found for given board')
            quit()

        best_moves = BS.find_best_moves()
        return sol, best_moves
    except:
        print()
        logging.error('Something went wrong. Were your inputs valid?')
        quit()

def main():
    try:     
        try:
            print("""                                                                                                 
 _____ _____ _____    _ _ _ _____ _____ _____ __    _____    _____ _____ __    _____ _____ _____ 
|  _  |     |     |  | | | |  _  |   __|   __|  |  |   __|  |   __|     |  |  |  |  |   __| __  |
|   __|  |  |  |  |  | | | |     |   __|   __|  |__|   __|  |__   |  |  |  |__|  |  |   __|    -|
|__|  |_____|_____|  |_____|__|__|__|  |__|  |_____|_____|  |_____|_____|_____|\___/|_____|__|__|
                                                                                                 
""")
            sz, lt, cl = extract_file(argv[1])
            logging.info(f'Opened file {argv[1]}.')
            print(f'\nSize    : {sz}')
            print(f'Letters : {lt} // lenght: {len(lt)}')
            print(f'Colours : {cl} // length: {len(cl)}')
        except FileNotFoundError:
            logging.error('File not found')
            quit()
        except IndexError:
            logging.info('No file given. Enter manual input.')
            logging.info('Keyboard interrupt (Ctrl + C) to exit.')
            logging.info('P.S. Right click to paste string in terminal :)\n')

            sz = int(input('Enter size: '))
            logging.info(f"Letters string and colours string should be of length {int((sz + 1) * (3*sz - 1) * 0.25)}.")
            lt = parse_letters(input('Enter letters string: '))
            print(f'            ⮡ length: {len(lt)}')
            cl = parse_colours(input('Enter colours string: '))
            print(f'            ⮡ length: {len(cl)}')

            # sz = 7
            # lt = parse_letters('MLLNPOELYGYIBPLIADEOEOAEETTLRNEARAIDSRRC')
            # cl = parse_colours('wwgwgyywwwygwgggwgywyygwgggwgywyywwgwgwws')
        
        sol, moves = run(sz, lt, cl)
        
        logging.info(f'SOLUTION: {sol}')  
        logging.info('Best moves to reach it:')
        for move in moves:
            print(move)      
    except KeyboardInterrupt:
        print()
        logging.info('Keyboard Interrupt')
        logging.info('Exitting')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
    main()