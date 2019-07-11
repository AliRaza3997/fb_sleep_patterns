from bs4 import BeautifulSoup
from functools import reduce
from util.selenium_util import ParseUtil

from parser.buddies_list_parser import BuddiesListParser


class BuddyParser:

    @staticmethod
    def parse_profile_intro(element):
        intro_element = element.find_elements_by_xpath('//div[@id="profile_intro_card"]')

        if intro_element:
            intro_element = intro_element[0]
        else:
            print("BuddyParser#parse_profile_intro ERROR - profile intro not found")
            return None

        intro_items = intro_element.find_elements_by_xpath(
            './/div[@data-sigil="touchable profile-intro-card-log profile-intro-card-log touchable"]')

        parsed_intro_items = []
        for item in intro_items:
            item = item.find_elements_by_xpath("./div[2]/div[1]/div[1]/span")

            # Here, item has the following format
            # <span>
            #   key text
            #   <strong>
            #     <span>
            #       value text
            #     </span>
            #   </strong>
            # </span>
            key_text, value_text = None, None
            if item:
                # https://stackoverflow.com/questions/45238364/python-and-selenium-get-text-excluding-child-nodes-text
                # Since element.text returns text from all child nodes too, to get the immediate
                # node's text i.e key text in our case, we need to do a hack
                # Note: script should only work if element is the selenium driver
                text_script = "var r='';var C=arguments[0].childNodes;for(var n=0;n<C.length;n++){if(C[n].nodeType==Node.TEXT_NODE){r+=' '+C[n].nodeValue}}return r.trim()"
                key_text = element.execute_script(text_script, item[0])
                key_text = key_text.strip()  # it's also possible that the key text is empty

                # key_text = BeautifulSoup(item[0].get_attribute("innerHTML")).contents[0]
                value_span = item[0].find_elements_by_xpath(".//span")

                if value_span:
                    value_text = value_span[0].text

            parsed_intro_items.append([key_text, value_text])

        return parsed_intro_items

    @staticmethod
    def parse_mutual_friends_list(driver):
        return BuddiesListParser.parse_friend_list(driver, root_id="root")

    @staticmethod
    def parse_all_friends_list(driver):
        return BuddiesListParser.parse_friend_list(driver, root_id="root")

    @staticmethod
    def parse_about_work_or_edu(element):
        attrs = element.find_elements_by_xpath('.//span[not(child::span)]')

        items = []
        for _idx, attr in enumerate(attrs):
            if _idx == 0:
                link = ParseUtil.find_element_by_xpath(attr, "./a", lambda el: el.get_attribute("href"))
                text = ParseUtil.find_element_by_xpath(attr, "./a", lambda el: el.text)
                items.append({
                    "link": link,
                    "text": text
                })
            else:
                text = attr.text
                items.append({
                    "text": text
                })

        return items if items else None

    @staticmethod
    def parse_about_places_lived(element):
        items = element.find_elements_by_xpath('.//header/h4')
        result = []
        for _idx, item in enumerate(items):
            result.append(item.text)

        return result if result else None

    @staticmethod
    def parse_about_basic_info_or_contact_info_or_nicknames(element):
        value = ParseUtil.find_element_by_xpath(element, './div[1]', lambda el: el.text)
        key = ParseUtil.find_element_by_xpath(element, './div[2]/span', lambda el: el.text)

        return {key: value}

    @staticmethod
    def parse_about_relationship(element):
        return element.text

    @staticmethod
    def parse_about_timeline(element):
        about = element.find_elements_by_xpath('//div[@id="timelineBody"]')
        if about:
            about = about[0]
        else:
            print("BuddyParser#parse_about_timeline ERROR - about page could not reload")
            return None

        work, education, living, basic_info, nicknames, relationship = None, None, None, None, None, None

        work = ParseUtil.find_elements_by_xpath(about,
                                                '//div[@id="work"]/div[1]/div/div[1]/div[1]',
                                                BuddyParser.parse_about_work_or_edu)

        education = ParseUtil.find_elements_by_xpath(about,
                                                     '//div[@id="education"]/div[1]/div/div[1]/div[1]',
                                                     BuddyParser.parse_about_work_or_edu)

        living = ParseUtil.find_elements_by_xpath(about,
                                                  '//div[@id="living"]/div[1]/div',
                                                  BuddyParser.parse_about_places_lived)

        contact_info = ParseUtil.find_elements_by_xpath(about,
                                                        '//div[@id="contact-info"]/div[1]/div/div[1]',
                                                        BuddyParser.parse_about_basic_info_or_contact_info_or_nicknames)

        if contact_info:
            contact_info = reduce(lambda x, y: dict(x, **y), contact_info)

        basic_info = ParseUtil.find_elements_by_xpath(about,
                                                      '//div[@id="basic-info"]/div[1]/div/div[1]',
                                                      BuddyParser.parse_about_basic_info_or_contact_info_or_nicknames)

        if basic_info:
            basic_info = reduce(lambda x, y: dict(x, **y), basic_info)

        nicknames = ParseUtil.find_elements_by_xpath(about,
                                                     '//div[@id="nicknames"]/div[1]/div/div[1]',
                                                     BuddyParser.parse_about_basic_info_or_contact_info_or_nicknames)

        if nicknames:
            nicknames = reduce(lambda x, y: dict(x, **y), nicknames)

        relationship = ParseUtil.find_elements_by_xpath(about,
                                                        '//div[@id="relationship"]/div[1]/div/div[1]',
                                                        BuddyParser.parse_about_relationship)

        return {
            "work": work,
            "education": education,
            "living": living,
            "contact_info": contact_info,
            "basic_info": basic_info,
            "nicknames": nicknames,
            "relationship": relationship
        }
