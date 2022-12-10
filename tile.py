from termcolor import colored
from selenium.webdriver.remote.webelement import WebElement

class Tile:
    letter: str
    colour: str
    web_element: WebElement
    
    def __init__(self, web_element) -> None:
        self.web_element = web_element
        self.letter = self.web_element.get_attribute('innerHTML')
        self.update_colour()

    def __str__(self) -> str:
        return colored(f'{self.letter}', f'{self.colour}')

    def __format__(self, __format_spec: str) -> str:
        return format(str(self), __format_spec)

    def __repr__(self) -> str:
        return f'Tile({self.letter}, {self.colour}, {self.web_element})'

    def update_colour(self) -> None:
        try:
            self.colour = list(set(self.web_element.get_dom_attribute("class").split(" ")) & set(['green', 'yellow']))[0]
        except:
            self.colour = 'white'