from api_plugin.sams_science import SamsApi
from config.config import Config
from main.dataset import Dataset
from main.log import Log
import time


class Application:
    def __init__(self):
        self.is_data_posted = False
        self.log = Log()
        self.api = SamsApi()
        self.config = Config()
        self.config_data = self.config.get_config_data()
        self.repost_seconds = int(self.config_data['INTERVAL']['repost_seconds'])
        self.app_wait_time = int(self.config_data['INTERVAL']['app_wait_seconds'])

        self.data = Dataset()
        self.dataset = dict()

    def take_dataset(self):
        self.dataset = ""
        self.dataset = self.data.get_dataset()

    def start(self):
        while True:
            print("take dataset...")
            self.take_dataset()

            if self.log.has_log_files():
                print("has log files...")
                self.log.post_log_files(self.dataset)
            else:
                response = self.api.call(self.dataset)
                if response:
                    print("Dataset posted!")
                else:
                    print("Dataset posting failed. Statuscode: {0}".format(response))
                    self.is_data_posted = False  # reset is data posted
                    print("log dataset")
                    self.log.insert(self.dataset)  # log dataset
                    while not self.is_data_posted:
                        print("try to post dataset...")
                        self.is_data_posted = self.api.call(self.dataset)
                        print("wait {0} seconds...".format(self.repost_seconds))
                        time.sleep(self.repost_seconds)
            time.sleep(int(self.app_wait_time))


