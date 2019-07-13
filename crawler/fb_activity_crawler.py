import random
from time import sleep
import pendulum
import os

from util.saver.active_buddies_saver import ActiveBuddiesSaver
from crawler.fb_crawler import FacebookCrawler
from parser.active_buddies_parser import ActiveBuddiesParser
from util.logger import Logger


class ActiveBuddiesCrawler(FacebookCrawler):
    """Crawls Facebook to extract the online status of friends.

    """

    def __init__(self, browser, credentials, dump_dir, log_dir):
        """
        Parameters
        ----------
        browser : :obj:Browser
            Browser object for navigating through web content.
        credentials : dict
            Dictionary containing the Facebook email and password for login.

        """

        FacebookCrawler.__init__(self, browser, credentials, dump_dir, log_dir)

        # Initialize logger
        Logger.init_logger(os.path.join(self._log_dir, 'app.log'))
        self.set_logger("crawler")

        # Create buddies saver for saving records
        self._saver = ActiveBuddiesSaver(self._dump_dir)

    def set_logger(self, name):
        self.logger = Logger.get_logger(name)
        self.logger.debug("Logger initialized")

    def crawl(self):
        """Crawls Facebook to extract the online status of friends.

        Gets the buddylist page of facebook every 3-3.5min (infinitely) and logs the list of online friends
        along with timestamp.

        """

        driver = self._browser.driver

        while True:
            try:
                driver.get("https://mobile.facebook.com/buddylist.php")
                sleep(8)  # wait for 8 seconds for the page to load
                driver.save_screenshot(os.path.join(self._screen_shots_dir, "online_friends.png"))

                # parse and save
                active_buddies = ActiveBuddiesParser.parse_active_buddies(driver)

                fn = self._saver.record({
                    "timestamp": str(pendulum.now()),
                    "buddies": active_buddies
                })

                self.logger.info("New record (%d online friends) saved at %s", len(active_buddies), fn)

                sleep(random.randint(60*2 + 30, 60*3 + 30))  # wait between 3-3.5 minutes
            except Exception as e:
                self.logger.error(e)
                raise e
