

import statistics
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from util.vector.curve_util import CurveUtil


class ActivityAnalyzer:

    def __init__(self, buddies, verbose=False):
        self.buddies = buddies
        self.days = None
        self._verbose = verbose
        self._activities_cache = None

        self.__init()

    def __init(self):
        self._find_all_days()

    def _find_all_days(self):
        days = set()
        for name in self.buddies:
            _, buddy = self.buddies[name]

            days = days.union(buddy.days)

        self.days = self.buddies.sort_days(days)

    def get_activity_maps(self, days=None, reload=False):
        if days is None: days = self.days

        if not reload and self._activities_cache:
            return self._activities_cache

        activities = {}

        if self._verbose: print('[Calculating activity maps]')
        for name in tqdm(list(self.buddies), disable=not self._verbose):
            _, buddy = self.buddies[name]

            activity_maps = buddy.get_activity_maps()
            activities[name] = activity_maps

        self._activities_cache = activities

        return activities

    def count_online_friends(self, days=None):
        if days is None: days = self.days
        count = {}

        activities = self.get_activity_maps()

        if self._verbose: print('[Calculating online count]')
        for name in tqdm(list(activities), disable=not self._verbose):
            _, buddy = self.buddies[name]
            buddy_days = buddy.days
            activity = activities[name]
            day_to_activity = {day_name: act for day_name, act in activity}

            for day in buddy_days:
                # skip if day is not in given days
                if day not in days:
                    continue

                # create key if doesn't exist
                if day not in count:
                    count[day] = []

                # find activity map for the day
                count[day].append(day_to_activity[day])

        # sum over axis=0 to get the count
        for day in count:
            count[day] = np.sum(np.array(count[day]), axis=0)


        # sort days array
        sorted_days = self.buddies.sort_days(list(count.keys()))

        return [(day, count[day]) for day in sorted_days]

    def plot_online_count(self, data=None, days=None):
        if days is None: days = self.days
        if data is None: data = self.count_online_friends(days)

        available_days, online = zip(*data)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        for _idx, day in enumerate(available_days):
            y = online[_idx]
            x = np.arange(len(y))

            y = CurveUtil.gaussian_smooth(y, sigma=8)

            ax.plot(x, y, label=day)

            ax.set_xticks(np.arange(0, len(y)+1, len(y)/24))  # +1 in len(y)+1 allows last point to be inclusive
            ax.set_xticklabels([str(i)+"h" for i in np.arange(0, 24)])

            ax.set_ylabel('No. of online friends')
            ax.set_xlabel('Hour of day')

        # get mean of online count
        y_mean = np.mean(online, axis=0)
        y_mean = CurveUtil.gaussian_smooth(y_mean)

        # plot mean online count as area graph
        ax.fill_between(x, y_mean, color="skyblue", alpha=0.4, label='Mean')

        # set legend
        ax.legend(loc='lower right', prop={'size': 15})

        fig.set_figwidth(20)
        fig.set_figheight(10)

    def plot_online_per_day(self, days=None):
        if days is None:
            days = self.days

        activities = self.get_activity_maps()  # returns a dict of pairs (buddy_name, activity per day)
        online_time = {day: [] for day in days}

        # Calculate time per day for each friend
        for name, activity in list(activities.items()):  # loop over acitivity for each buddy
            activity = list(filter(lambda x: x[0] in days, activity))
            if len(activity) == 0:
                continue

            buddy_days, activity_map = list(zip(*activity))

            # find buddy online time for each day
            buddy_time = np.sum(np.array(activity_map), axis=1) * 24*60 / len(activity_map[0])
            buddy_time = buddy_time.tolist()

            for _idx, day in enumerate(buddy_days):
                online_time[day].append(buddy_time[_idx])

        # Calculate mean online time for each day
        total_online_time = []
        for day in days:
            total_online_time.append((day, statistics.mean(online_time[day]) if online_time[day] else 0))

        # ----- Ploting -----
        days, online_time = zip(*total_online_time)

        # Setup figure
        fig, ax = plt.subplots()
        fig.set_figwidth(15)
        fig.set_figheight(8)

        # Plot time per day
        ax.bar(np.arange(len(online_time)), online_time)

        # Display time per day one each bar
        for i, v in enumerate(online_time):
            ax.text(i-0.11, v+1, str(round(v/60, 1))+'hr', color='black')

        plt.xticks(np.arange(len(online_time)), [day.split(" ")[0] for day in days])

