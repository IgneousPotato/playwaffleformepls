import colorama

from termcolor import colored
from selenium.webdriver.remote.webelement import WebElement


class Tile:
    letter: str
    colour: str

    def __init__(self, letter: str, colour: str) -> None:
        self.letter = letter
        self.colour = colour

    def __str__(self) -> str:
        colorama.init()
        return colored(f'{self.letter}', f'{self.colour}')

    def __format__(self, __format_spec: str) -> str:
        return format(str(self), __format_spec)

    def __repr__(self) -> str:
        return f'Tile({self.letter}, {self.colour})'

    def update_colour(self, colour) -> None:
        self.colour = colour


class Web_Tile(Tile):
    web_element: WebElement

    def __init__(self, web_element: WebElement) -> None:
        self.web_element = web_element
        self.letter = self.web_element.get_attribute('innerHTML')
        self.update_colour()

    def __repr__(self) -> str:
        return f'Web_Tile({self.letter}, {self.colour}, {self.web_element})'

    def update_colour(self) -> None:
        try:
            self.colour = list(set(self.web_element.get_dom_attribute(
                "class").split(" ")) & set(['green', 'yellow']))[0]
        except:
            self.colour = 'white'
