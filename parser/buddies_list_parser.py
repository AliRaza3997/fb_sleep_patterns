
from tqdm import tqdm


class BuddiesListParser:

    def __int__(self):
        pass

    @staticmethod
    def parse_friend_list(driver, root_id=None):
        """
        Parses friends list page to extract listed friends.\
        Note: Scrolling should be done before calling this function
              to load full list of friends in the page
        """
        # get friends list with following structure
        # <div>
        #   <h3>
        #     <a href="/manisha.tanwani.16">
        #       Manisha Tanwani
        #     </a>
        #   </h3>
        #   <div data-sigil="m-friend-request-highlight-notice">
        #     ...
        #   </div>
        # </div>

        list_query = '//div[@data-sigil="undoable-action"]/div[2]/div[1]'
        if root_id:
            list_query = '//div[@id="%s"]//div[@data-sigil="undoable-action"]/div[2]/div[1]' % root_id

        buddy_list = driver.find_elements_by_xpath(list_query)

        print("[Parse friends list (total=%s)]" % len(buddy_list), flush=True)
        friends = []

        for _idx in tqdm(range(len(buddy_list))):
            buddy = buddy_list[_idx]

            try:
                name = buddy.find_elements_by_xpath('./h3/a') or buddy.find_elements_by_xpath('./h1/a')
                num_mutual_friends = buddy.find_elements_by_xpath(
                    './/div[@data-sigil="m-add-friend-source-replaceable"]')

                username = None
                if name:
                    username = name[0].get_attribute("href")
                    username = username.split("/")[-1] if username else None
                    name = name[0].text

                if num_mutual_friends:
                    num_mutual_friends = num_mutual_friends[0].text
                    num_mutual_friends = [int(s) for s in num_mutual_friends.split() if s.isdigit()]
                    num_mutual_friends = num_mutual_friends[0] if num_mutual_friends else None
                else:
                    num_mutual_friends = None

                friends.append({
                    "name": name,
                    "username": username,
                    "mutual_friends": num_mutual_friends
                })

            except Exception as e:
                raise e

        return friends
