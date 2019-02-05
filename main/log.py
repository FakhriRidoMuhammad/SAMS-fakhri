import json
import os
import time
from api_plugin.sams_science import SamsApi


class Log:
    def __init__(self):
        self.path = '/home/pi/log/'
        self.api = SamsApi()
        self.status = []
        self.files = os.listdir(self.path)

    def insert(self, json_data):
        print("insert data...")
        files = os.listdir(self.path)
        if len(files) != 0:
            file = int(
                len([name for name in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, name))])) + 1
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
            self.files = os.listdir(self.path)
            print("log dataset...")
            self.insert(dataset)
            self.list_dir()
            print("list directory: {0}".format(self.files))
            while self.has_log_files():
                for x in range(len(self.files)):
                    file = self.read_file(self.path + str(self.files[x]))
                    print("try to post data")
                    if self.api.call(file):
                        print("status code ok! Delete file...")
                        os.remove(self.path + str(self.files[x]))
                    time.sleep(5)

            print("all log files posted")
            return True

        except Exception as e:
            print(e)
