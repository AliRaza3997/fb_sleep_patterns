#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""main.py

This script visualizes the online activity of the Facebook friends.

Example
-------
Script can be executed as following::

    $ python visualize.py --data_dir ./dumped_data

"""

__author__ = "Ali Raza"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ali Raza"
__email__ = "aliraza3997@gmail.com"
__status__ = "Development"

import os
import argparse
import matplotlib.pyplot as plt
from itertools import groupby
from collections import OrderedDict
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

from analysis.buddies.buddies import Buddies
from analysis.analysis_util.data_util import ActivityDataReader
from analysis.config.buddies_timezone import BUDDIES_TIMEZONE
from util.logger import Logger


def print_grouped_names(names):
    names = sorted(names)
    groups = groupby(names, key=lambda x: x[0])

    grouped_names = OrderedDict()
    for key, group in groups:
        grouped_names[key] = list(group)

    for key, names in grouped_names.items():
        disp = ", ".join([n.title() for n in names[:3]])
        if len(names) > 3:
            disp += ", and {} more".format(len(names)-3)

        print("{}: {}".format(key, disp))


def input_friend_name(available_names):
    # Input friend name from user
    name_completer = FuzzyWordCompleter(available_names)
    name = prompt('Enter friend name: ', completer=name_completer)

    return name


def argument_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--data_dir', type=str,
                        help='Raw data directory where data was dumped. Default is ./dumped_data')

    return parser.parse_args()


if __name__ == "__main__":
    args = argument_parser()
    data_dir = args.data_dir if args.data_dir is not None else './dumped_data'

    # Initialize the logger
    log_dir = "./logs"
    Logger.init_logger(os.path.join(log_dir, "visualize.log"))

    # Read online activity data
    reader = ActivityDataReader(data_dir)
    data = reader.read()

    # Create and parse Buddies
    friends = Buddies(data, buddy_tzs=BUDDIES_TIMEZONE, adjust_tz=True, verbose=True, cache=False)

    # Print friend names
    print_grouped_names(friends.names)
    print("{} friends found. Please select a name to create the sleep graph.".format(len(friends.names)))

    while True:
        # Input friend name from user
        name = input_friend_name(friends.names)
        name, buddy = friends[name]

        if buddy is not None:
            # Plot the activity graph
            plt.figure(figsize=(20, 8), dpi=80, facecolor='w', edgecolor='k')
            buddy.plot_activity(days=buddy.days[-5:],
                                title="Online activity of {}".format(name.title()))
