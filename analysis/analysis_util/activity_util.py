

import numpy as np


class ActivityUtil:

    @staticmethod
    def __idx_to_time(start_idx, end_idx, unit_mnt):
        start_hr, start_mnt = start_idx * unit_mnt // 60, start_idx * unit_mnt % 60
        end_hr, end_mnt = end_idx * unit_mnt // 60, end_idx * unit_mnt % 60 + unit_mnt

        return ["%.2d:%.2d" % (start_hr, start_mnt),
                "%.2d:%.2d" % (end_hr, end_mnt)]

    @staticmethod
    def find_sleep_time(day_map, unit_mnt):
        t = ActivityUtil.calculate_max_offline_gaps(day_map)[0]
        slp_s, slp_e, slp_count = t

        sleep_time = ActivityUtil.__idx_to_time(slp_s, slp_e, unit_mnt)

        return {
            "time": sleep_time,
            "indices": [slp_s, slp_e],
            "count": slp_count * unit_mnt
        }

    @staticmethod
    def __idx_to_time_multi(start_idx, end_idx, bf_midn_items, af_midn_items, unit_min=3):
        is_start_af_midn = start_idx >= bf_midn_items
        is_end_af_midn = end_idx >= bf_midn_items

        if not is_start_af_midn:  # before midnight
            start_hr, start_mnt = (bf_midn_items-start_idx) * unit_min // 60, (bf_midn_items-start_idx) * unit_min % 60
            start_hr, start_mnt = 24-start_hr, 60-start_mnt
            start_hr = start_hr-1 if start_mnt > 0 else start_mnt  # if minutes is non-zeros, need to go back one hour
        else:  # after midnight
            start_idx -= bf_midn_items
            start_hr, start_mnt = start_idx * unit_min // 60, start_idx * unit_min % 60

        if not is_end_af_midn:  # before midnight
            end_hr, end_mnt = (bf_midn_items-end_idx) * unit_min // 60, (bf_midn_items-end_idx) * unit_min % 60
            end_hr, end_mnt = 24-end_hr, 60-end_mnt
            end_hr = end_hr-1 if end_mnt > 0 else end_hr  # if minutes is non-zeros, need to go back one hour
        else:  # after midnight
            end_idx -= bf_midn_items
            end_hr, end_mnt = end_idx * unit_min // 60, end_idx * unit_min % 60 + unit_min

        return ["%.2d:%.2d" % (start_hr, start_mnt), "%.2d:%.2d" % (end_hr, end_mnt)]

    @staticmethod
    def find_sleep_time_multi_day(day1_map, day2_map, search_start_hr, search_end_hr, unit_mnt, verbose=False):
        # Total values in activity map
        num_bins = len(day1_map)

        # Search start and end indices
        fs_idx = search_start_hr * 60 // unit_mnt
        fe_idx = search_end_hr * 60 // unit_mnt

        if verbose: print("Before and after indices", fs_idx, fe_idx)

        bf_midn = day1_map[fs_idx:]
        af_midn = day2_map[:fe_idx+1]
        night = np.concatenate((bf_midn, af_midn))

        if verbose: print("Before and after items: ", len(bf_midn), len(af_midn))

        sleep_time = ActivityUtil.calculate_max_offline_gaps(night, num_max=1)[0]
        slp_s, slp_e, slp_count = sleep_time

        if verbose: print("Sleep start and end: ", slp_s, slp_e)

        sleep_time = ActivityUtil.__idx_to_time_multi(slp_s, slp_e, len(bf_midn), len(af_midn))

        return {
            "time": sleep_time,
            "indices": [slp_s, slp_e],
            "count": slp_count * unit_mnt,
            "before_midnight_num": len(bf_midn),
            "after_midnight_num": len(af_midn)
        }

    @staticmethod
    def calculate_max_offline_gaps(y, num_max=1):
        start, end = -1, -1
        inds = []

        for i in range(len(y)):

            if y[i] == 0:  # empty
                if start == -1:
                    start = i
            elif y[i] == 1:  # filled
                end = i - 1

                if start != -1:
                    inds.append((start, end))

                start, end = -1, -1

        inds = np.array(inds)
        count = (inds[:, 1] +1)  - inds[:, 0]

        sort_ind = np.argsort(count)[::-1]

        inds = inds[sort_ind, :]
        count = count[sort_ind]

        max_ind = np.argmax(count)

        return np.column_stack((inds[:num_max, :], count[:num_max]))
