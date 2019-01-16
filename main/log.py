import json
import os
import time
from api_plugin.sams_science import Api


class Log:
    def __init__(self):
        self.path = '/home/pi/log/'
        self.api = Api()
        self.status = []
        self.files = os.listdir(self.path)

    def insert(self, json_data):
        files = os.listdir(self.path)
        if len(files) != 0:
            file = max(files)
            file = int(file[:-5]) + 1
        else:
            file = int(1)
        try:
            with open(self.path + str(file) + ".json", 'w') as f:
                json.dump(json_data, f)
                f.close()
        except Exception as e:
            print(e)

    def list_dir(self):
        self.files = os.listdir(self.path)

    @staticmethod
    def read_file(path):
        f = open(path, "r")

        return f.read()

    def has_log_files(self):
        if not os.listdir(self.path):
            return False
        else:
            return True

    def post_log_files(self, dataset):
        try:
            print("try post log files...")
            self.insert(dataset)
            print("log dataset...")
            self.list_dir()
            print("list directory: {0}".format(self.files))
            while self.has_log_files():
                for x in range(len(self.files)):
                    file = self.read_file(self.path + str(self.files[x]))
                    print("try to post data")
                    if self.api.post_dataset(file):
                        print("status code ok! Delete file...")
                        os.remove(self.path + str(self.files[x]))
                    time.sleep(5)

            print("all log files posted")

        except Exception as e:
            print(e)
