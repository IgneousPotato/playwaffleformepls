from selenium.webdriver import ActionChains


class Player:
    actions: ActionChains
    
    def __init__(self, driver) -> None:
        self.actions = ActionChains(driver)
    
    def move_element(self, source, target) -> None:
        self.actions.drag_and_drop(source, target).perform()

    def play_instructions(self, dict, instructions) -> None:
        pass
