import logging

from termcolor import colored
from selenium.webdriver.remote.webelement import WebElement

class Tile:
    # id: int
    letter: str
    colour: str
    web_element: WebElement
    
    def __init__(self, web_element) -> None:
        self.web_element = web_element
        self.letter = web_element.get_attribute('innerHTML')
        try:
            self.colour = web_element.get_dom_attribute("class").split(" ")[3]
        except:
            self.colour = 'white'

    def __str__(self) -> str:
        return colored(f'{self.letter}', f'{self.colour}')

    def __repr__(self) -> str:
        return f'Tile({self.web_element}, {self.letter}, {self.colour})'
    
    def get_letter(self) -> str:
        return self.letter

    def get_colour(self) -> str:
        return self.colour 

    def update_colour(self, new_col) -> None:
        if new_col == 'green' or 'yellow' or 'white':
            self.colour = new_col
        else:
            logging.INFO('Tile cannot be changed to that colour. Tiles can only be green, yellow, or white.')
