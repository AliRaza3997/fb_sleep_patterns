
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Browser:
    """Wrapper class for selenium web driver.

    Creates an instance of the Chrome web driver and initializes it.

    Attributes
    ----------
    driver : webdriver.Chrome
        Instance of chrome web driver
    """

    def __init__(self, driver_path, init=False):
        """

        Parameters
        ----------
        driver_path : str
            Path to chrome driver executable.
        init : bool, optional
            True, if driver should be initialized. Alternatively, self.init() can be
            called for initializing the driver later.

        """

        self._chrome_driver_ex = os.path.join(driver_path)
        self.driver = None

        if init:
            self.init()

    def init(self, verbose=False):
        #: chrome.Options: setup chrome browser options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(options=chrome_options, executable_path=self._chrome_driver_ex)

        if verbose:
            print("Browser#init driver initialized")

    def get(self, _url):
        self.driver.get(_url)
        return self.driver

    def close(self):
        self.driver.quit()


class DriverUtil:

    @staticmethod
    def get(driver, _url, post_wait=2):
        driver.get(_url)

        if post_wait:
            sleep(post_wait)

    @staticmethod
    def infinite_scroll_to_bottom(driver, pause_time=2, tries=1, iter_callback=None, verbose=False):
        """
        Scrolls to the bottom of infinite page until page length keeps increasing.

        Parameters
        ----------
        driver
            Webdriver
        pause_time : float
            Pause time after each scroll operation.
        tries : int
            Number of tries to do for determining the end of page.
        iter_callback : func
            Callback function after each iteration
        verbose

        Returns
        -------
        int
            Number of times page was successfully scrolled.

        """

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        i = 0
        fail_tries = 0

        # until scroll tries for new content not reached try limit
        while fail_tries < tries:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # new content not found
                fail_tries += 1
            else:
                fail_tries = 0
                i += 1

            last_height = new_height

            if iter_callback and fail_tries < tries:
                iter_callback(i)

            if verbose and fail_tries < tries:
                print("No. of times scrolled=%s" % str(i))

        return i


class ParseUtil:

    @staticmethod
    def find_element_by_xpath(element, query, callback=None):
        el = element.find_elements_by_xpath(query)

        if callback:
            el = callback(el[0]) if el else None
        else:
            el = el[0] if el else None

        return el

    @staticmethod
    def find_elements_by_xpath(element, query, callback=None):
        items = element.find_elements_by_xpath(query)

        if items:
            if callback:
                items = [callback(item) for item in items]
        else:
            items = None

        return items

