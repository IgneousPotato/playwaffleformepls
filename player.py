import logging

from time import sleep
from selenium.webdriver import ActionChains
from board import Board


class Player:
    board: Board
    
    def __init__(self, board) -> None:
        self.board = board
    
    def move_tile(self, idx1, idx2) -> None:
        logging.info(f"Moving {idx1} ({self.board.tiles[idx1]}) to {idx2} ({self.board.tiles[idx2]})")
        sleep(0.1)
        self.board.change_tiles(idx1, idx2)
        
    def play_instructions(self, dict, instructions) -> None:
        pass

class Web_Player(Player):
    actions: ActionChains
    
    def __init__(self, action_driver, board) -> None:
        super().__init__(board)
        self.actions = action_driver

    def move_tile(self, idx1, idx2) -> None:
        tile1 = self.board.tiles[idx1].web_element
        tile2 = self.board.tiles[idx2].web_element
        self.actions.drag_and_drop(tile1, tile2).perform()
        super().move_tile(idx1, idx2)
