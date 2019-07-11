
from abc import ABC, abstractmethod
from time import sleep


class FacebookCrawler(ABC):
    """Base class for crawling facebook.

    """

    def __init__(self, browser, credentials):
        """
        Parameters
        ----------
        browser : :obj:Browser
            Browser object for navigating through web content.
        credentials : dict
            Dictionary containing the Facebook email and password for login.

        """

        self._browser = browser
        self._credentials = credentials

    @property
    def browser(self):
        """Browser: Instance of Browser for navigating web pages."""
        return self._browser

    def login(self, post_wait=10):
        """Logs in to Facebook.

        Parameters
        ----------
        post_wait : int
            No. of seconds to wait after logging in.

        Returns
        -------
        bool
            True if logging in successful, False otherwise.

        """

        if self._credentials:
            driver = self._browser.get('https://mobile.facebook.com/')
            print("BuddyScrapper#login opened facebook")
            sleep(4)

            username_box = driver.find_element_by_id('m_login_email')
            username_box.send_keys(self._credentials["email"])
            print("BuddyScrapper#login email id entered")
            sleep(2)

            password_box = driver.find_element_by_id('m_login_password')
            password_box.send_keys(self._credentials["password"])
            print("BuddyScrapper#login password entered")
            sleep(2)

            login_box = driver.find_elements_by_xpath('//button[@name="login"]')
            if len(login_box):
                login_box[0].click()
                sleep(post_wait)  # wait for page to reload after login, needs more time
                driver.save_screenshot("logged_in.png")
                print("BuddyScrapper#login logged in, screenshot saved")
            else:
                print("BuddyScrapper#login login button not found")
        else:
            print("BuddyScrapper#login fb credentials found to be None")

    @abstractmethod
    def crawl(self):
        """Crawls Facebook to extract the required information.

        """

        raise NotImplementedError
