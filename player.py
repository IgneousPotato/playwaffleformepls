import logging

from time import sleep
from selenium.webdriver import ActionChains
from board import Board


class Player:
    actions: ActionChains
    board: Board
    
    def __init__(self, action_driver, board) -> None:
        self.actions = action_driver
        self.board = board
    
    def move_tile(self, idx1, idx2) -> None:
        tile1 = self.board.tiles[idx1].web_element
        tile2 = self.board.tiles[idx2].web_element
        logging.info(f"Moving {idx1} ({self.board.tiles[idx1]}) to {idx2} ({self.board.tiles[idx2]})")

        sleep(0.1)
        self.actions.drag_and_drop(tile1, tile2).perform()
        self.board.change_tiles(idx1, idx2)
        print(self.board)
        
    def play_instructions(self, dict, instructions) -> None:
        pass
