#!/usr/bin/env python
import logging
import argparse

from time import sleep
from seleniumrequests import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options

from tile import Web_Tile
from board import Web_Board
from player import Web_Player
from solver import Solver
from driver import Driver

def main() -> None:
    # THIS IS SPECIFICALLY FOR THE DAILY WAFFLE.
    try:
        headless = args.headless
        automatic = args.automatic
        
        logging.info(f'Headless: {headless}. Automatic: {automatic}\n')
        logging.info('Waiting for page to load.')

        browserOpts = Options()
        browserOpts.headless = headless
        browser = Firefox(options=browserOpts)
    
        driver = Driver(url='https://wafflegame.net/', driver=browser)
        driver.load_dynamic_page()
        solution = driver.get_todays_solution()
        
        browser.maximize_window()   
        try:
            sleep(3)
            driver.click_elem(type=By.CLASS_NAME, tag="css-b2i6wm")
            logging.info("Opened privacy options")
            
            driver.click_elem(type=By.CLASS_NAME, tag="css-1vx625n")
            logging.info("Rejected all")
            
            driver.click_elem(type=By.CLASS_NAME, tag="css-1litn2c", mul=True)
            logging.info("Saved privacy options")
        except:
            pass
        finally:
            driver.delete_elem(tag="help modal modal--show")
            logging.info("Closed help information")

        tiles = []
        num = 22
        xpath = "/html/body/div[3]/div[2]/main[1]/div[2]/div[2]/div"
        while num < 43:
            try:
                element = browser.find_element(By.XPATH, f"{xpath}[{num}]")
                
                tile = Web_Tile(element)
                tiles.append(tile)   

                num += 1    
            except:
                xpath = "/html/body/div[4]/div[2]/main[1]/div[2]/div[2]/div" # idk why but it sometimes changes the first div in the xpath?
                num = 22

        game_num = browser.find_element(By.CLASS_NAME, 'game-number').get_attribute('innerHTML')
        print(f'\n{game_num}')

        board = Web_Board(browser, 5)
        board.add_tiles(tiles)
        print(board)

        words = []      # words from https://www.bestwordlist.com/
        with open('five_letter_words.txt') as flw:
            for line in flw:
                words.extend(line.split())

        action_driver = ActionChains(browser)
        player = Web_Player(action_driver, board)

        BS = Solver(board, words)
        poss_sol = BS.solve()
    
        instructions = []
        for k, v in poss_sol.items():
            if BS.get_solved_letters(v) == solution:
                instructions = BS.find_best_moves(v)
               
                logging.info(f'SOLUTION #{k}: {v}')  
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

        player.run_instructions(instructions, automatic = automatic)
        
        if not headless:
            logging.info('Press ENTER to close.')
            input()

    except KeyboardInterrupt:
        exit()

    finally:
        try:
            browser.close()
            pass
        except:
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plays today's puzzle at Wafflegame.net")
    parser.add_argument('-H', '--headless', metavar='headless', help='open browser or not', action=argparse.BooleanOptionalAction)
    parser.add_argument('-a', '--automatic', metavar='automatic', help='play moves automatically or not', action=argparse.BooleanOptionalAction)
    parser.set_defaults(headless=True, automatic=True)
    
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
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
