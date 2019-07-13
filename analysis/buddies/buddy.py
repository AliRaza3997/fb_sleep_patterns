

import numpy as np
import pendulum
import matplotlib.pyplot as plt
from itertools import groupby

from analysis.analysis_util.activity_util import ActivityUtil
from util.list_util import ListUtil


class Buddy:

    def __init__(self, timestamps):
        self.dates = timestamps

        self._unit_mnt = 3  # time in minutes for each bin
        self.days = None
        self.data = None

        self._init()

    def _init(self):
        self._process_data()

    def _process_data(self):
        # group items by the day of month
        groups = groupby(self.dates, lambda d: d.format('dd DD/MM/YY'))
        groups = {key: list(value) for key, value in groups}

        # sort group keys
        keys = groups.keys()
        date_keys = [pendulum.from_format(key, 'dd DD/MM/YY') for key in keys]
        date_keys = sorted(date_keys)
        sorted_keys = [dk.format('dd DD/MM/YY') for dk in date_keys]

        self.days = sorted_keys
        self.data = groups

    def in_tz(self, tz):
        self.dates = [dt.in_tz(tz) for dt in self.dates]

    def get_day_activity_map(self, day):
        time = list(map(lambda d: (int(d.format('YY')),
                                   int(d.format('MM')),
                                   int(d.format('DD')),
                                   d.format('dd'),
                                   int(d.format('HH')),
                                   int(d.format('mm'))), self.data[day]))

        # create linear space from 0-24h*60m with a gap of self._unit_mnt min
        bins = np.arange(0, 24*60 + self._unit_mnt, self._unit_mnt)

        active = [t[-2]*60 + t[-1] for t in time]

        active_bin_ind = np.digitize(active, bins)
        active_bin_ind = sorted(list(set(active_bin_ind)))

        x = np.arange(0, len(bins))
        y = np.zeros((len(bins)))
        y[active_bin_ind] = 1

        return y, bins

    def get_activity_maps(self, days=None):
        if days is None:
            days = self.days

        activity = []

        for day in days:
            y, bins = self.get_day_activity_map(day)
            activity.append((day, y))

        return activity

    def find_sleep_time(self, days=None):
        if days is None: days = self.days
        search_st_hour, search_en_hr = 20, 12

        times = []

        # Calculate sleep time for second to last day
        for idx, day in enumerate(days):
            if idx != len(days)-1:
                day1_act, bins = self.get_day_activity_map(day)
                day2_act, bins = self.get_day_activity_map(days[idx+1])

                t = ActivityUtil.find_sleep_time_multi_day(
                    day1_act, day2_act, search_st_hour, search_en_hr, self._unit_mnt)

                times.append(t)

        # Calculate sleep time for the first day
        day_act, bins = self.get_day_activity_map(days[0])
        idx0_time = ActivityUtil.find_sleep_time(day_act, self._unit_mnt)
        times.insert(0, idx0_time)

        return times

    def plot_activity(self, days=None, activity=None, title="Online Status"):
        if activity is not None and days is None:
            raise Exception("Buddy#plot_activity Missing argument days (required if activity is given)")

        # Initialize some data
        if days is None: days = self.days
        num_days, y = len(days), activity

        # Get activity if not provided
        if y is None:
            y = [self.get_day_activity_map(day)[0] for day in days]
            y = ListUtil.flatten(y)

        # Setup figure
        ax1 = plt.subplot(1, 1, 1)

        # No. of ticks for each day
        num_x_ticks = 4

        # Plot
        ax1.bar(np.arange(len(y)), y, alpha=0.8, align='center', width=1)

        # ----- Setup first x-axis ticks -----
        x_ticks = []
        for i in range(num_days):
            # +1 in 24+1 in last days ticks allows last point to be inclusive
            x_ticks.extend([str(i)+"h" for i in
                            np.arange(0, 24+1 if i==num_days-1 else 24, 24/num_x_ticks, dtype=np.uint8)])

        # +1 in len(y)+1 allows last point to be inclusive
        x_ticks_pos = np.arange(0, len(y)+1, len(y)/num_days/num_x_ticks)

        # Setup first x-axis ticks
        ax1.set_xticks(x_ticks_pos)
        ax1.set_xticklabels(x_ticks)
        ax1.set_xlabel('Hour of Day')

        # ----- Setup second x axis ticks -----
        ax2 = ax1.twiny()
        x2_ticks_pos = np.arange(len(y)/num_days/2, len(y), len(y)/num_days)

        ax2.set_xticks(x2_ticks_pos)
        ax2.set_xlim(ax1.get_xlim())
        ax2.set_xticklabels(days)

        ax2.xaxis.set_ticks_position('bottom')
        ax2.xaxis.set_label_position('bottom')
        ax2.spines['bottom'].set_position(('outward', 36))

        ax2.set_xlabel('Date')

        ax1.set_ylabel("Online")
        ax1.set_yticks([])

        if title:
            plt.title(title)

        plt.show()

        return [ax1, ax2]

    def plot_sleep(self, days=None):
        if days is None:
            days = self.days

        # Get activity map for particular days' data
        activity = [self.get_day_activity_map(day)[0] for day in days]
        y = ListUtil.flatten(activity)

        sleep_times = self.find_sleep_time(days)

        # Plot online activity
        axes = self.plot_activity(days, y, title="")
        ax1 = axes[0]

        for idx, slp_time in enumerate(sleep_times):
            indices, formatted_time, slp_count = slp_time["indices"], slp_time["time"], slp_time["count"]
            bf_midn = slp_time["before_midnight_num"] if "before_midnight_num" in slp_time else 0

            # Adjust indices for multi day sleep
            indices = [i + idx*481 - bf_midn for i in indices]

            # Find mid index of sleep and total hours
            mid_idx = (indices[1] - indices[0]) // 2
            total_hours = round(slp_count / 60.0, 1)

            # Text to be displayed
            hr_text = "%s hr(s) \nsleep" % total_hours
            t_text = "%s - %s" % (formatted_time[0], formatted_time[1])

            if idx == 0:
                night = "../%s" % days[idx].split(" ")[0]
            else:
                night = "%s/%s" % (days[idx-1].split(" ")[0], days[idx].split(" ")[0])

            params = {
                "style": "italic",
                "horizontalalignment": "center"
            }

            # Draw sleep hours and time texts
            ax1.text(indices[0] + mid_idx, 0.6, night, **params, weight="bold")
            ax1.text(indices[0] + mid_idx, 0.5, hr_text, **params)
            ax1.text(indices[0] + mid_idx, 0.4, t_text, **params, rotation=90)

            # Draw background of sleep cells
            sleep_bg = (76/255, 146/255, 195/255, 0.3)
            plt.bar(np.arange(indices[0], indices[1]+1), np.ones((indices[1]-indices[0]+1)), color=sleep_bg, align='center', width=1)

        ax1.set_ylabel("Online")
        ax1.set_yticks([])

        plt.show()
