
from bs4 import BeautifulSoup


class ActiveBuddiesParser:

    def __int__(self):
        pass

    @staticmethod
    def parse_active_buddies(driver):
        buddy_list = driver.find_elements_by_xpath('//div[@id="mobile_buddylist"]')

        text = None
        if len(buddy_list):
            text = buddy_list[0].get_attribute('innerHTML')
        else:
            print("BuddyScrapper#__parse_buddy_page active buddy element not found")
            return

        soup = BeautifulSoup(text)
        buddies = soup.findAll('div', {"class": "title"})

        return [buddy.text for buddy in buddies]

