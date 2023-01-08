#!/usr/bin/env python
import logging
import argparse
import os

from time import sleep
from seleniumrequests import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import JavascriptException

from tile import Web_Tile
from board import Web_Board
from player import Web_Player
from solver import Solver


def main() -> None:
    """
    Plays wafflegame.net
    """
    mode, headless, automatic = args.mode, args.headless, args.automatic

    size, num, num_end = 5, 22, 43
    file = 'five_letter_words.txt'
    match mode:
        case 'daily':
            puzzle_type = 'state'
            xpath = "/html/body/div[3]/div[2]/main[1]/div[2]"
        case 'archive':
            puzzle_type = 'agame'
            xpath = "/html/body/div[3]/div[2]/main[5]/div[1]"
            if not args.number:
                archive_num = input("Enter archive number: ")
            else:
                archive_num = args.number
        case 'deluxe':
            size, num, num_end, puzzle_type = 7, 41, 81, 'deluxe'
            xpath = "/html/body/div[3]/div[2]/main[2]/div[2]"
            file = 'seven_letter_words.txt'

    words = []      # words from https://www.bestwordlist.com/
    with open(file, encoding='utf-8') as flw:
        for line in flw:
            words.extend(line.split())

    logging.info('Mode: %s. Headless: %s. Automatic: %s\n',
                 mode, headless, automatic)
    logging.info('Loading wafflegame.net')

    browser_opts = Options()
    browser_opts.headless = headless
    browser = Firefox(options=browser_opts, service_log_path=os.devnull)
    browser.get('https://wafflegame.net/')
    browser.maximize_window()

    try:
        sleep(3)
        browser.execute_script(
            """document.querySelector("[class=' css-b2i6wm']").click()""")
        browser.execute_script(
            """document.querySelector("[class=' css-1vx625n']").click()""")
        browser.execute_script(
            """document.querySelectorAll("[class=' css-1litn2c']").forEach(el=>el.click())""")
        browser.execute_script(
            """document.querySelector("#qc-cmp2-container").remove()""")
    except JavascriptException:
        pass
    finally:
        wait = True
        while wait:
            try:
                browser.execute_script(
                    """document.querySelectorAll("[class='button--close icon-button']")
                       .forEach(el=>el.click())""")
                wait = False
            except JavascriptException:
                sleep(0.5)
                continue

    logging.info("Closed privacy and help tabs")

    match mode:
        case 'daily':
            pass
        case 'archive':
            # FOR ARCHIVE
            browser.execute_script(
                """document.querySelector("[class='menu__item menu__item--archive']").click()""")
            # need wait till page loads
            wait = True
            while wait:
                try:
                    browser.execute_script(
                        f"""document.querySelector("[data-id='{archive_num}']").click()""")
                except JavascriptException:
                    sleep(0.5)
                    continue
                wait = False
        case 'deluxe':
            # FOR DELUXE
            browser.execute_script(
                """document.querySelector("[class='menu__item menu__item--deluxe']").click()""")
            sleep(0.5)

    logging.info("Loaded selected puzzle DOM.")

    solution = browser.execute_script(f"""
                            var l = JSON.parse(window.localStorage.getItem("{puzzle_type}"));
                            return l['solution']
                            """)
    tiles = [Web_Tile(browser.find_element(By.XPATH, f"{xpath}/div[2]/div[{num}]"))
             for num in list(range(num, num_end))]
    board = Web_Board(browser, size)
    board.add_tiles(tiles)

    print(
        f"\n{browser.find_element(By.XPATH, f'{xpath}/div[1]').get_attribute('innerHTML')}")
    print(board)

    logging.info("Solving puzzle.")

    action_driver = ActionChains(browser)
    player = Web_Player(action_driver, board)
    solver = Solver(board, words)
    poss_sol = solver.solve()

    instructions = []
    for _, val in poss_sol.items():
        if solver.get_solved_letters(val) == list(solution):
            instructions = solver.find_best_moves(val)

            logging.info('SOLUTION: %s', val)
            logging.info('Best moves to reach it:')
            for move in instructions:
                print(move)
        else:
            continue
    print()

    if automatic:
        logging.info('Playing moves automatically.')
    else:
        logging.info('Press enter to play next move.')
        input()

    player.run_instructions(instructions, automatic=automatic)

    if not headless:
        logging.info('Press ENTER to close.')
        input()
        browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Plays today's puzzle at Wafflegame.net")
    parser.add_argument('-m', '--mode', metavar='mode',
                        type=str, help='daily, archive, or deluxe')
    parser.add_argument('-n', '--number', metavar='number',
                        type=int, help="ignored unless mode set to 'archive'")
    parser.add_argument('-hd', '--headless', metavar='headless',
                        help='open browser or not', action=argparse.BooleanOptionalAction)
    parser.add_argument('-a', '--automatic', metavar='automatic',
                        help='play automatically or not', action=argparse.BooleanOptionalAction)
    parser.set_defaults(mode='daily', headless=False, automatic=False)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s:%(asctime)s - %(message)s')
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

    main()
