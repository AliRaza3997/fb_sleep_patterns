
import os
import glob
import pendulum
import json


class ActiveBuddiesSaver:
    """Dumps active buddies information to JSON in disk.

    """

    def __init__(self, output_dir):
        """

        Parameters
        ----------
        output_dir : str
            Path to output directory for dumping the crawled data.

        """

        self._output_dir = output_dir

        # create records directory
        os.makedirs(self._output_dir, exist_ok=True)

    def record(self, data):
        """Dumps provided data to disk as JSON.

        Finds out the next possible filename and dumps data to disk as JSON.
        Note
        ----

        Parameters
        ----------
        data : dict
            Dictionary with activity data and timestamp for dumping.

        Returns
        -------
        str
            Filename to which data was dumped

        """

        timestamp = data["timestamp"]
        dt = pendulum.parse(timestamp)

        # create dir name
        dump_dir = self._find_dump_dir(dt)

        files = glob.glob("{}/*.json".format(dump_dir))
        file_nums = [int(os.path.split(fn)[-1].split(".")[0]) for fn in files]
        file_nums.sort(reverse=True)

        fn = None
        if len(file_nums):
            fn = os.path.join(dump_dir, "%s.json" % str(file_nums[0]+1))
        else:
            fn = os.path.join(dump_dir, "%s.json" % str(1))

        with open(fn, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        return fn

    def _find_dump_dir(self, dt):
        """Finds the name of the dump dir based on timestamp.

        Data is dumped in specific directory for each day. This function
        returns the name of the directory for the provided timestamp.
        Also creates the directory if it doesn't exist.

        Parameters
        ----------
        dt : pendulum.datetime.DateTime
            Timestamp for which directory name is needed.

        Returns
        -------
        str
            Directory name for the given timestamp.

        """
        dir_name = os.path.join(self._output_dir, dt.format('YYMMDD'))
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        return dir_name
