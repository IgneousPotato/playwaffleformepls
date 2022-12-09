import logging

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from tile import Tile
from board import Board
from player import Player
from scrapper import Scrapper


def main():
    try:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
        
        browserOpts = Options()
        browserOpts.headless = True
        browser = webdriver.Firefox(options=browserOpts)
        browser.maximize_window()
    
        driver = Scrapper(url='https://wafflegame.net/', driver=browser)
        driver.load_dynamic_page()
        driver.extract_html()
        
        try:
            sleep(10)
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
            sleep(10)
            driver.delete_elem(tag="vm-skin vm-skin-left")
            driver.delete_elem(tag="vm-skin vm-skin-right")
            logging.info("Ew, bye ads.")
        except:
            logging.info("Damnit. Ads live. Yuck.")''' 
            
        tiles = []
        for num in range(22, 43, 1):
            element = browser.find_element(By.XPATH, f"/html/body/div[4]/div[2]/main[1]/div[2]/div[2]/div[{num}]")            
            tile = Tile(element)
            tiles.append(tile)
        
        board = Board(5)
        # player = Player(browser)
        # player.move_bit(a, b)

    finally:
        try:
            browser.close()
            pass
        except:
            pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s - %(message)s')
    main()
