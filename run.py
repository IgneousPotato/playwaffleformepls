#!/usr/bin/env python
import logging

from time import sleep
from seleniumrequests import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options

from tile import Web_Tile
from board import Web_Board
from player import Web_Player
from solver import Solver
from scrapper import Scrapper

def main() -> None:
    try:
        # headless = True
        headless = False

        browserOpts = Options()
        browserOpts.headless = headless
        browser = Firefox(options=browserOpts)
    
        driver = Scrapper(url='https://wafflegame.net/', driver=browser)
        driver.load_dynamic_page()
        
        if not headless:
            browser.maximize_window()
            try:
                sleep(5)
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

            '''try:
                driver.delete_elem(tag="vm-skin vm-skin-left")
                driver.delete_elem(tag="vm-skin vm-skin-right")
                logging.info("Ew, bye ads.")
            except:
                pass'''


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
        
        instructions = {}

        if len(poss_sol.items()) > 1:
            logging.info('FOUND MULTIPLE SOLUTIONS')

        for k, v in poss_sol.items():
            print()
            instructions[k] = BS.find_best_moves(v)
            
            move_count = len(instructions[k])
            if move_count != 10 and move_count != 20:
                logging.info(f'FOLLOWING SOLUTION IS VALID BUT INVALID ON WAFFLEGAME.NET AS IT CAN BE REACHED IN {move_count} MOVES!!!!')
                
            logging.info(f'SOLUTION #{k}: {v}')  
            logging.info('Best moves to reach it:')
            for move in instructions[k]:
                print(move)    
        
        print()
        if len(poss_sol.items()) > 1:
            picked_sol = input('Enter solution number (#) to follow moves: ')
        else:
            picked_sol = 0
        
        logging.info(f'Selected solution: {poss_sol[picked_sol]}')    
        logging.info(f'Moves: {instructions[picked_sol]}')
        
        player.run_instructions(instructions[picked_sol], automatic = False)
        
    finally:
        try:
            logging.info('Press ENTER to close.')
            input()
            browser.close()
            pass
        except:
            pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
    print("""                                       
 _____ __    _____ _____ _____ _____   
|  _  |  |  |     |     |   __|_   _|  
|     |  |__| | | |  |  |__   | | |    
|__|__|_____|_|_|_|_____|_____| |_|    
 _ _ _ _____ _____ _____ __    _____   
| | | |  _  |   __|   __|  |  |   __|  
| | | |     |   __|   __|  |__|   __|  
|_____|__|__|__|  |__|  |_____|_____|  
 _____ _____ __    _____ _____ _____   
|   __|     |  |  |  |  |   __| __  |  
|__   |  |  |  |__|  |  |   __|    -|  
|_____|_____|_____|\___/|_____|__|__|  
                                    """)
    main()
