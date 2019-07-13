

import pendulum
from tqdm import tqdm
import numpy as np
import pickle
import os

from analysis.buddies.buddy import Buddy
from util.list_util import ListUtil
from util.logger import Logger


class Buddies:

    def __init__(self, raw_data, buddy_tzs=None, adjust_tz=True, verbose=False, cache=True):
        self._buddy_tzs = buddy_tzs
        self._raw_data = raw_data
        self._adjust_tz = adjust_tz
        self._verbose = verbose

        self.names = None
        self.buddies = {}

        self.data = None
        self._cache_enabled = cache
        self._cache_fn = "./analysis/tmp/buddies_cache.pkl"

        self._init()

    def _init(self):
        if self._cache_enabled and os.path.exists(self._cache_fn):
            self.load()
            return

        self.names = self.__get_buddy_names()
        self.buddies = self.__create_buddies()

        if self._adjust_tz:
            self.__adjust_timezones()

        if self._cache_enabled:
            self.dump()

    def dump(self):
        if self._verbose: print("Buddies#dump Caching data to %s" % self._cache_fn)

        data = {
            "names": self.names,
            "buddies": self.buddies
        }

        with open(self._cache_fn, "wb") as f:
            pickle.dump(data, f)

    def load(self):
        if self._verbose: print("Buddies#dump Loading data from cache at %s" % self._cache_fn)

        with open(self._cache_fn, "rb") as f:
            data = pickle.load(f)

            self.names = data["names"]
            self.buddies = data["buddies"]

    def __get_buddy_names(self):
        buddy_names = [record["buddies"] for record in self._raw_data if record["buddies"]]
        buddy_names = set(ListUtil.flatten(buddy_names))
        buddy_names = [name.lower() for name in buddy_names]

        return buddy_names

    def __create_buddies(self):
        Logger.get_logger().info("Parsing buddies data")

        data = {name: [] for name in self.names}

        for _idx, record in enumerate(tqdm(self._raw_data, disable=not self._verbose)):
            if record["buddies"] is None:
                Logger.get_logger().debug("Buddies found to be None")
                continue

            buddies = [name.lower() for name in record["buddies"]]
            ts = record["timestamp"]

            for name in buddies:
                data[name].append(pendulum.parse(ts))

        Logger.get_logger().info("Generating buddies")
        for name in tqdm(data, disable=not self._verbose):
            data[name] = Buddy(data[name])

        return data

    def __iter__(self):
        return (name for name in self.names)

    def __getitem__(self, query):
        query = query.lower()

        # check if friend exist
        found = [name.find(query) >= 0 for name in self.names]
        matched_names = np.array(self.names)[found]

        perfect_matches = [name for name in matched_names if len(name) == len(query)]
        name = None
        
        if len(perfect_matches):
            if len(perfect_matches) > 1:
                Logger.get_logger().warning("Duplicate names found, returning first...".format(query))

            name = perfect_matches[0]
        else:  # no perfect match found
            if len(matched_names):
                if len(matched_names) == 1:
                    name = matched_names[0]
                elif len(matched_names) > 1:
                    Logger.get_logger().warning("Multiple matches. Please "
                                                "provide more specific query".format(query))
            else:
                Logger.get_logger().warning("No matches found for {}".format(query))

        return name, self.buddies[name] if name is not None else None

    def __adjust_timezones(self):
        default_tz = 'Asia/Karachi'

        other_tz_friends = []
        default_tz_friends = self.names

        if self._buddy_tzs:
            other_tz_friends = ListUtil.flatten(list(self._buddy_tzs.values()))
            default_tz_friends = list(set(self.names) - set(other_tz_friends))

        Logger.get_logger().info("Correcting timezones")
        _ = [self.buddies[name].in_tz(default_tz) for name in tqdm(default_tz_friends, disable=not self._verbose)]

        if self._buddy_tzs is None:
            return

        for tz, names in self._buddy_tzs.items():
            _ = [self.buddies[name].in_tz(tz) for name in names if name in self.buddies]

    def sort_days(self, days):
        date_keys = [pendulum.from_format(key, 'dd DD/MM/YY') for key in days]
        date_keys = sorted(date_keys)
        sorted_keys = [dk.format('dd DD/MM/YY') for dk in date_keys]

        return sorted_keys
