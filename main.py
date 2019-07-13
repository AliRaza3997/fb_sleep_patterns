#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""main.py

This script runs the Facebook crawler (infinitely) and dumps the data to disk as JSON.

Example
-------
Script can be executed as following::

    $ python main.py --email <email id> --password <password>'

"""

__author__ = "Ali Raza"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Ali Raza"
__email__ = "aliraza3997@gmail.com"
__status__ = "Development"

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

    log_dir = './logs'
    dump_dir = './dumped_data'

    crawler = ActiveBuddiesCrawler(browser, {
        "email": args.email,
        "password": args.password
    }, dump_dir, log_dir)

    crawler.login()
    crawler.crawl()
