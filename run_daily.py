#!/usr/bin/env python
import logging

from sys import argv
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
        headless = True
        try:
            match argv[1]:
                case 'True':
                    pass
                case 'False':
                    headless = False
                case _:
                    logging.info(f"I don't know what {argv[1]} means. Running in headless mode.") 
        except:
            pass

        browserOpts = Options()
        browserOpts.headless = headless
        browser = Firefox(options=browserOpts)
    
        driver = Driver(url='https://wafflegame.net/', driver=browser)
        driver.load_dynamic_page()
        solution = driver.get_todays_solution()
        
        if not headless:
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

            try:
                driver.delete_elem(tag="vm-skin vm-skin-left")
                driver.delete_elem(tag="vm-skin vm-skin-right")
                logging.info("Ew, bye ads.")
            except:
                pass

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
    
        instructions = []
        for k, v in poss_sol.items():
            if BS.get_solved_letters(v) == solution:
                instructions = BS.find_best_moves(v)
               
                logging.info(f'SOLUTION #{k}: {v}')  
                logging.info('Best moves to reach it:')
                for move in instructions:
                    print(move)    
            else:
                logging.error("Today's solution not found... Dunno why. Do it yourself I guess. Soz.")
        
        if headless == True:
            automatic = True
        else:
            exit = True
            while exit:
                check = input('Run automatically? Y or N: ')
                match check:
                    case 'Y':
                        automatic = True
                        exit = False
                    case 'N':
                        automatic = False
                        exit = False
                    case _:
                        logging.error('Just answer it properly.')
        
        player.run_instructions(instructions, automatic = automatic)
        
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
