
from abc import ABC, abstractmethod
from time import sleep
import os


class FacebookCrawler(ABC):
    """Base class for crawling facebook.

    """

    def __init__(self, browser, credentials, dump_dir, log_dir):
        """
        Parameters
        ----------
        browser : :obj:Browser
            Browser object for navigating through web content.
        credentials : dict
            Dictionary containing the Facebook email and password for login.
        log_dir : str
            Path to log directory.

        """

        self._browser = browser
        self._credentials = credentials
        self._dump_dir = dump_dir
        self._log_dir = log_dir
        self._screen_shots_dir = os.path.join(self._log_dir, 'screen_shots')
        self.logger = None

        self._init()

    @property
    def browser(self):
        """Browser: Instance of Browser for navigating web pages."""
        return self._browser

    def _init(self):
        os.makedirs(self._dump_dir, exist_ok=True)
        os.makedirs(self._log_dir, exist_ok=True)
        os.makedirs(self._screen_shots_dir, exist_ok=True)

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
            self.logger.info("Loaded login page")
            sleep(4)

            username_box = driver.find_element_by_id('m_login_email')
            username_box.send_keys(self._credentials["email"])
            self.logger.info("Email id entered")
            sleep(1)

            password_box = driver.find_element_by_id('m_login_password')
            password_box.send_keys(self._credentials["password"])
            self.logger.info("Password entered")
            sleep(1)

            login_box = driver.find_elements_by_xpath('//button[@name="login"]')
            if len(login_box):
                login_box[0].click()
                sleep(post_wait)  # wait for page to reload after login, needs more time
                driver.save_screenshot(os.path.join(self._screen_shots_dir, "logged_in.png"))
                self.logger.info("Login successful :), screen-shot saved")
            else:
                self.logger.error("Login failed :), login button not found")
        else:
            self.logger.error("Login failed :), credentials not set")

    @abstractmethod
    def crawl(self):
        """Crawls Facebook to extract the required information.

        """

        raise NotImplementedError
