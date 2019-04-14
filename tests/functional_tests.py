from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from timeit import default_timer as timer


class FunctionalTest1(TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            options=options,
            executable_path='./chromedriver'
        )

    def tearDown(self):
        self.driver.close()
        self.driver.quit()

    @staticmethod
    def severe_and_unexpected(message):
        return message['level'] == 'SEVERE' and 'favicon.ico - Failed to load' not in message['message']

    def wait_for_page_to_initialise(self, timeout=10):
        start = timer()
        while True:
            if self.driver.execute_script("return window.initialEvalIsCompleted;"):
                break
            if timer() - start > timeout:  # Time in seconds
                raise Exception("page didn't finish loading quickly enough")
            else:
                time.sleep(0.1)

    def test_no_errors_index(self):
        """Test that there are no JavaScript errors."""
        self.driver.get("http://localhost:8009")

        browser_log = self.driver.get_log('browser')
        browser_errors = [message for message in browser_log if self.severe_and_unexpected(message)]
        self.assertListEqual(browser_errors, [])

    def test_no_errors_other_pages(self):
        """Test that there are no JavaScript errors."""
        self.driver.get("http://localhost:8009/1-1-elements.html")
        self.wait_for_page_to_initialise()

        all_divs = self.driver.find_elements_by_tag_name("div")
        scheme_divs = [div for div in all_divs if div.id.startswith("scheme")]

        # Trigger the onFocus callback
        code_mirror = self.driver.find_elements_by_xpath('//div/div[@class="CodeMirror"]')
        code_mirror[0].click()
        code_mirror[1].click()

        browser_log = self.driver.get_log('browser')
        browser_errors = [message for message in browser_log if self.severe_and_unexpected(message)]
        self.assertListEqual(browser_errors, [])
