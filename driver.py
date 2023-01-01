from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class Driver:
    def __init__(self, url: str, driver: webdriver = None) -> None:
        self.html = url
        if driver != None:
            self.driver = driver
        else:
            self.driver = None

    def load_dynamic_page(self) -> None:
        # "Tried to use dynamic page loading without a webdriver."
        self.driver.get(self.html)
        self.page_content = self.driver.page_source
        self.soup = BeautifulSoup(self.page_content, 'html.parser')

    def print_html(self) -> None:
        print(self.soup.prettify())

    def click_elem(self, type: By, tag: str, mul = False) -> None:
        if mul:
            a = self.driver.find_elements(type, tag)
            for i in a:
                try:
                    i.click()
                except:
                    pass
        else:
            self.driver.find_element(By.CLASS_NAME, tag).click()
        
    def delete_elem(self, tag: str) -> None:
        self.driver.execute_script(f"""
            var l = document.getElementsByClassName("{tag}")[0];
            l.parentNode.removeChild(l);
            """)

    def get_todays_solution(self) -> list:
        solution = self.driver.execute_script("""var l = JSON.parse(window.localStorage.getItem("state"));
                                                 return l['solution']""")
        return solution