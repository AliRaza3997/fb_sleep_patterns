

from bs4 import BeautifulSoup


def print_html(element):
    soup = BeautifulSoup(element.get_attribute("outerHTML"))
    print(soup.prettify())
