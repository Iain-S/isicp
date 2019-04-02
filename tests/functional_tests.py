from unittest import TestCase
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
import time


class FunctionalTest1(TestCase):
    def setUp(self):
        self.options = Options()
        # self.options.add_argument("--headless")
        self.browser = webdriver.Firefox(
            options=self.options, executable_path='./geckodriver'
        )
        pass

    def tearDown(self):
        self.browser.close()
        self.browser.quit()

    def test_no_js_errors(self):
        """Test that there are no JavaScript errors."""
        self.browser.get("http://localhost:8009")
        # time.sleep(1)
        # print(self.browser.get_log('browser'))
