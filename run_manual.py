#!/usr/bin/env python
import logging
import argparse

from tile import Tile
from board import Board
from solver import Solver


def extract_file(file_name: str) -> int | list | list:
    if file_name.endswith('.txt'):
        with open(file_name, encoding='utf8') as file:
            size = int(file.readline().strip('\n'))
            letters = file.readline().strip('\n')
            colours = file.readline()
    else:
        logging.error('File type is incorrect. It must be a .txt file.')
        quit()

    return size, parse_letters(letters), parse_colours(colours)


def parse_letters(ltr_str: str) -> list:
    if ltr_str is None:
        return None
    return list(ltr_str.upper())


def parse_colours(col_str: str) -> list:
    if col_str is None:
        return None

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
    with open(dict_file, encoding='utf8') as flw:
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

        solver = Solver(board, words)
        poss_sol = solver.solve()

        if poss_sol is None:
            logging.info('No valid solution found for given board')
            exit()
        best_moves = {}

        for k, sol in poss_sol.items():
            best_moves[k] = solver.find_best_moves(sol)

        return poss_sol, best_moves
    except Exception as exp:
        print()
        logging.error('Were your inputs valid?')
        logging.error('%s', exp)
        exit()


def main() -> None:
    try:
        print("""
 _____ __    _____ __ __    _ _ _ _____ _____ _____ __    _____   
|  _  |  |  |  _  |  |  |  | | | |  _  |   __|   __|  |  |   __|  
|   __|  |__|     |_   _|  | | | |     |   __|   __|  |__|   __|  
|__|  |_____|__|__| |_|    |_____|__|__|__|  |__|  |_____|_____|  
 _____ _____ _____    _____ _____    _____ __    _____            
|   __|     | __  |  |     |   __|  |  _  |  |  |   __|           
|   __|  |  |    -|  | | | |   __|  |   __|  |__|__   |           
|__|  |_____|__|__|  |_|_|_|_____|  |__|  |_____|_____|           
                                                            """)

        if args.file is not None:
            if args.size is not None or args.letters is not None or args.colours is not None:
                logging.info(
                    "Ignored all other arguments except for ['-f', --file']")

            try:
                sz, lt, cl = extract_file(args.file)
                logging.info('Opened file %s.', args.file)

            except FileNotFoundError:
                logging.error('File not found')
                quit()

        else:
            sz, lt, cl = args.size, parse_letters(
                args.letters), parse_colours(args.colours)

            if args.size is None:
                sz = int(input('Enter size: '))
                logging.info("Letters string and colours string should be of length %s.", int(
                    (sz + 1) * (3*sz - 1) * 0.25))

            if args.letters is None:
                lt = parse_letters(input('Enter letters string: '))
                print(f'            ⮡ length: {len(lt)}')

            if args.colours is None:
                cl = parse_colours(input('Enter colours string: '))
                print(f'            ⮡ length: {len(cl)}')

        print(f'\nSize    : {sz}')
        print(f'Letters : {lt} // length: {len(lt)}')
        print(f'Colours : {cl} // length: {len(cl)}')

        sol, moves = run(sz, lt, cl)

        if len(sol.items()) > 1:
            logging.info('FOUND MULTIPLE SOLUTIONS')

        for key, val in sol.items():
            print()
            move_count = len(moves[key])
            stars = ' for 5 stars'

            logging.info('SOLUTION #%s: %s', key, val)
            if move_count != 10 and move_count != 20:
                logging.info(
                    'IT IS VALID BUT INVALID ON WAFFLEGAME.NET AS IT CAN BE REACHED IN MINIMUM OF %s MOVES!!', move_count)
                stars = ''

            logging.info('Possible %s moves to solve it%s:', move_count, stars)
            for move in moves[key]:
                print(move)

    except KeyboardInterrupt:
        print()
        logging.info('Keyboard Interrupt')
        logging.info('Exitting')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plays today's puzzle at Wafflegame.net")
    parser.add_argument('-f', '--file', metavar='file', help='open file')

    group = parser.add_argument_group()
    group.add_argument('-s', '--size', metavar='size',
                       type=int, help='size of board')
    group.add_argument('-l', '--letters', metavar='letters',
                       type=str, help='letters on the board')
    group.add_argument('-c', '--colours', metavar='colours',
                       type=str, help='colours of letters on the board')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s:%(asctime)s - %(message)s')
    main()
