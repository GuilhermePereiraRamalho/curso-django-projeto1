from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.common.by import By

from utils.browser import make_chrome_browser

import time


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=10):
        time.sleep(seconds)

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )
