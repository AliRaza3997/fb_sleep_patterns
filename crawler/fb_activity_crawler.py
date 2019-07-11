import random
from time import sleep
import pendulum

from util.saver.active_buddies_saver import ActiveBuddiesSaver
from crawler.fb_crawler import FacebookCrawler
from parser.active_buddies_parser import ActiveBuddiesParser


class ActiveBuddiesCrawler(FacebookCrawler):
    """Crawls Facebook to extract the online status of friends.

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

        FacebookCrawler.__init__(self, browser, credentials)

        # buddies saver for saving records
        self._saver = ActiveBuddiesSaver("./dumped_data")

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

                # parse and save
                active_buddies = ActiveBuddiesParser.parse_active_buddies(driver)

                fn = self._saver.record({
                    "timestamp": str(pendulum.now()),
                    "buddies": active_buddies
                })

                time_now = pendulum.now()

                print("[%s] BuddyScrapper#scrap_active_buddies new record saved at %s" % (time_now.format("HH:mm:ss"), fn))

                sleep(random.randint(60*2 + 30, 60*3 + 30))  # wait between 3-3.5 minutes
            except Exception as e:
                print(e)
                exit(0)
