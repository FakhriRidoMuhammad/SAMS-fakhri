import json
import os


class Log:
    def __init__(self):
        self.path = '/home/pi/log/'

    def insert(self, json_data):
        files = os.listdir(self.path)
        file = max(files)
        print(int(file[:-5]))


log = Log()
example = [{'test': 123}]
log.insert(example)
