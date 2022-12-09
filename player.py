from selenium.webdriver import ActionChains


class Player:
    # _driver: webdriver
    _actions: ActionChains
    
    def __init__(self, driver) -> None:
        # self._driver = driver
        self._actions = ActionChains(driver)
    
    def move_element(self, source, target) -> None:
        self._actions.drag_and_drop(source, target).perform()
