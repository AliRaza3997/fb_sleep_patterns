# -*- coding: utf-8 -*-
"""main.py

This script runs the Facebook crawler and dumps the data to disk as JSON.

Example
-------
Script can be executed as following::

    $ python main.py --email <email id> --password <password>'

"""

import argparse

from crawler.fb_activity_crawler import ActiveBuddiesCrawler
from util.selenium_util import Browser


def argument_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--email', type=str, help='Email id for Facebook')
    parser.add_argument('--password', type=str, help='Password for Facebook')

    return parser.parse_args()


if __name__ == "__main__":
    args = argument_parser()

    if args.email is None or args.password is None:
        print('Usage: python main.py --email <email id> --password <password>')
        exit(1)

    driver_path = './lib/chromedriver'
    browser = Browser(driver_path, init=True)

    crawler = ActiveBuddiesCrawler(browser, credentials={
        "email": args.email,
        "password": args.password
    })

    crawler.login()
    crawler.crawl()
