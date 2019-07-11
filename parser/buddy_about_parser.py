
from util.selenium_util import ParseUtil
from tqdm import tqdm


class BuddyAboutParser:

    @staticmethod
    def get_sections(element, section_name=None, verbose=False):
        """
        Returns a particular section element in the page (with header parsed)
        if section_name is not None, else returns list of all the sections'
        elements.

        :param element:
        :param section_name:
        :param verbose:
        :return:
        """

        # get all timeline sections in the page
        sections = ParseUtil.find_elements_by_xpath(element,
                                                    '//div[@id="timelineBody"]//div[@data-sigil="profile-card"]')

        if verbose:
            print("%s sections found" % (len(sections) if sections else 0))

        if sections is None or len(sections) == 0:
            return []

        parsed_sections = []

        for section in sections:
            header = BuddyAboutParser.parse_section_header(section)
            parsed_sections.append({
                    "header": header,
                    "content": section
            })

        if section_name:
            for section in parsed_sections:
                if section["header"]["name"] == section_name:
                    return section
        else:
            return parsed_sections

    @staticmethod
    def parse_section_header(element, verbose=False):
        # parse  link
        link = ParseUtil.find_element_by_xpath(element, './/header//a')

        href, name = None, None

        if link:
            href = link.get_attribute("href")

        # parse section name
        header = ParseUtil.find_element_by_xpath(element, './/header')

        if header is not None:
            name = header.text.split("\n")[-1].strip()

        return {
            "url": href,
            "name": name
        }

    @staticmethod
    def parse_section(element, section_type='list'):
        """

        Parameters
        ----------
        element
        section_type : str
            type of section ['list', 'tile']

        Returns
        -------

        """

        if section_type == "list":
            return BuddyAboutParser.parse_section_item_list(element)
        elif section_type == "tile":
            return BuddyAboutParser.parse_section_item_tile(element)
        else:
            raise Exception("Invalid section_type=%s" % section_type)

    @staticmethod
    def parse_section_item_list(element):
        item_elements = ParseUtil.find_elements_by_xpath(element,
         './/header/following-sibling::div/div[1]//div[@data-sigil="m-timeline-collections-item marea"]')

        items = []
        if item_elements:
            for el in tqdm(item_elements):
                items.append(BuddyAboutParser.parse_section_item_list_element(el))

        return items

    @staticmethod
    def parse_section_item_list_element(element):
        link = ParseUtil.find_element_by_xpath(element, './a')
        if link:
            link = link.get_attribute("href")

        image = ParseUtil.find_element_by_xpath(element, './/div[@class="image"]')
        content = ParseUtil.find_element_by_xpath(element, './/div[@class="content"]')

        # get heading
        heading = ParseUtil.find_element_by_xpath(content, './div[1]/strong').text.strip()

        # get content items
        content_items = ParseUtil.find_elements_by_xpath(content,
                       './/*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::span]')

        if content_items:
            content_items = [c.text.strip() for c in content_items]

        return {
            "name": heading,
            "url": link,
            "content": content_items
        }

    @staticmethod
    def parse_section_item_tile(element, verbose=False):
        bquery = ".//header/following-sibling::div/div[1]"
        item_elements = ParseUtil.find_elements_by_xpath(element, '%s//a/parent::div' % bquery)

        items = []
        for item_el in tqdm(item_elements):
            link = ParseUtil.find_element_by_xpath(item_el, './a').get_attribute("href")
            name = item_el.find_element_by_xpath(
                                    './a/following-sibling::div').text

            items.append({
                "name": name,
                "url": link
            })

        return items
