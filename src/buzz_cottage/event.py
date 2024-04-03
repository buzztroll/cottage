import os
import random


class EventExec(object):
    def __init__(self, dir_path, suffix="sh"):
        self._dir_path = dir_path
        self._suffix = suffix

    def pick_one(self):
        file_list = []
        dir_list = os.listdir(self._dir_path)
        for i in dir_list:
            if i.endswith(self._suffix):
                file_list.append(i)
        return random.choice(file_list)


e = EventExec("/etc", suffix="conf")
print(e.pick_one())
