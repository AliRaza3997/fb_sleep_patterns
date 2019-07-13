
import os
import json

from tqdm import tqdm
from util.file_utils import FileUtil
from util.logger import Logger


class ActivityDataReader:

    def __init__(self, src_dir, verbose=False):
        self._src_dir = src_dir
        self.raw_data = None
        self.buddies = None
        self._verbose = verbose
        self.file_names = None

    def read(self):

        dirnames = FileUtil.get_dirs(self._src_dir, sort=True)
        file_names = []
        data = []

        Logger.get_logger().info("Reading data")

        for _dir in dirnames:
            file_names.extend(self.__get_fns(_dir))

        self.file_names = file_names

        for file_name in tqdm(file_names, disable=not self._verbose):
            with open(file_name, 'r') as f:
                record = json.load(f)
                data.append(record)

        self.raw_data = data
        self.__process()

        return self.raw_data

    def __process(self):
        self.__sanitize_raw_data()

    def __sanitize_raw_data(self):
        self.raw_data = [record for record in self.raw_data if record["buddies"]]

    def __get_fns(self, dir_name):
        return FileUtil.get_files_with_ext(dir_name, 'json', sort=True,
                                      sort_key=lambda x: int(os.path.split(x)[-1].split(".")[0]))
