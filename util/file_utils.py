
import glob
import os


class FileUtil:

    @staticmethod
    def get_dirs(dir_name, sort=False, sort_key=None):
        dirs = glob.glob(os.path.join(dir_name, "*/"))

        if sort:
            dirs.sort(key=sort_key)

        return dirs

    @staticmethod
    def get_files_with_ext(dir_name, ext, recursive=False, sort=False, sort_key=None):

        if recursive:
            query = "%s/**/*.%s" % (dir_name, ext)
        else:
            query = "%s/*.%s" % (dir_name, ext)

        files = glob.glob(query)

        if sort:
            files.sort(key=sort_key)

        return files
