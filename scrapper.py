import requests

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


class Scrapper:
    html: str

    _soup: BeautifulSoup
    _page_content: requests.models.Response
    _driver: webdriver

    def __init__(self, url, driver: webdriver = None) -> None:
        self.html = url
        if driver != None:
            self._driver = driver
        else:
            self._driver = None

    
    def load_static_page(self) -> None:
        self._page_content = requests.get(self.html, verify=False)

    def load_dynamic_page(self) -> None:
        # "Tried to use dynamic page loading without a webdriver."
        self._driver.get(self.html)
        self._page_content = self._driver.page_source
        
    def extract_html(self) -> None:
        self._soup = BeautifulSoup(self._page_content, 'html.parser')

    def print_html(self) -> None:
        print(self._soup.prettify())

    def click_elem(self, type, tag, mul = False) -> None:
        if mul:
            a = self._driver.find_elements(type, tag)
            for i in a:
                try:
                    i.click()
                except:
                    pass
        else:
            self._driver.find_element(By.CLASS_NAME, tag).click()
        
    def delete_elem(self, tag):
        self._driver.execute_script(f"""
            var l = document.getElementsByClassName("{tag}")[0];
            l.parentNode.removeChild(l);
            """)