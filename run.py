#!/usr/bin/env python
import logging

from seleniumrequests import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options

from tile import Web_Tile
from board import Web_Board
from player import Web_Player
from solver import Solver
from scrapper import Scrapper

def main():
    try:
        headless = True

        browserOpts = Options()
        browserOpts.headless = headless
        browser = Firefox(options=browserOpts)
    
        driver = Scrapper(url='https://wafflegame.net/', driver=browser)
        driver.load_dynamic_page()
        
        if not headless:
            browser.maximize_window()
            try:
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
        xpath_base = "/html/body/div[3]/div[2]/main[1]/div[2]/div[2]/div"
        
        while num < 43:
            try:
                xpath = f"{xpath_base}[{num}]"
                element = browser.find_element(By.XPATH, xpath)
                
                tile = Web_Tile(element)
                tiles.append(tile)   

                num += 1    
            except:
                xpath_base = "/html/body/div[4]/div[2]/main[1]/div[2]/div[2]/div" # idk why but it sometimes changes the first div in the xpath?
                num = 22

        board = Web_Board(browser, 5)
        board.add_tiles(tiles)

        words = []
        # words from https://www.bestwordlist.com/
        with open('five_letter_words.txt') as flw:
            for line in flw:
                words.extend(line.split())

        BS = Solver(board, words)

        action_driver = ActionChains(browser)
        player = Web_Player(action_driver, board)
        
        print(board)
        ans = BS.solve()
        logging.info(f'FINAL SOLUTION: {ans}')
        
    finally:
        try:
            browser.close()
            pass
        except:
            pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
    main()
