from termcolor import colored
from selenium.webdriver.remote.webelement import WebElement

class Tile:
    letter: str
    colour: str
    pos: list
    
    def __init__(self, letter, colour, pos) -> None:
        self.letter = letter
        self.colour = colour
        self.pos = pos

    def __str__(self) -> str:
        return colored(f'{self.letter}', f'{self.colour}')

    def __format__(self, __format_spec: str) -> str:
        return format(str(self), __format_spec)

    def __repr__(self) -> str:
        return f'Tile({self.letter}, {self.colour})'

    def update_col_pos(self, colour, pos) -> None:
        self.pos = pos
        self.colour = colour

class Web_Tile(Tile):
    web_element: WebElement

    def __init__(self, web_element) -> None:
        self.web_element = web_element
        self.letter = self.web_element.get_attribute('innerHTML')
        self.update_col_pos()
    
    def __repr__(self) -> str:
        return f'Web_Tile({self.letter}, {self.colour}, {self.web_element})'

    def update_col_pos(self) -> None:
        temp_pos = self.web_element.get_dom_attribute("data-pos")
        self.pos = (int(temp_pos[-2]), int(temp_pos[-8]))
        try:
            self.colour = list(set(self.web_element.get_dom_attribute("class").split(" ")) & set(['green', 'yellow']))[0]
        except:
            self.colour = 'white'