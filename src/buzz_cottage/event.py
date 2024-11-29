import logging
import os
import random


_g_logger = logging.getLogger(__file__)


class EventExec(object):
    def __init__(self, dir_path, suffix="sh"):
        self._dir_path = dir_path
        self._suffix = suffix

    def pick_one(self):
        file_list = []
        _g_logger.info(f"listing {self._dir_path}")
        dir_list = os.listdir(self._dir_path)
        for i in dir_list:
            _g_logger.info(f"found {i}")
            if i.endswith(self._suffix):
                file_list.append(i)
        return os.path.join(self._dir_path, random.choice(file_list))
