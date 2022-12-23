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
        self.board.change_tiles(idx1, idx2)
            
    def run_instructions(self, instructions: list, automatic: bool = True) -> None:
        for instruction in instructions:
            print(instruction[0], instruction[1])
            self.move_tile(instruction[0], instruction[1])
            print(self.board)

            if automatic == True:
                sleep(0.1)
            else:
                input()


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
