from api_plugin.sams_science import SamsApi
from config.config import Config
from main.dataset import Dataset
from main.log import Log
from main.error import ErrorLog
import time


class Application:
    def __init__(self):
        self.is_data_posted = False
        self.error = ErrorLog()
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
            try:
                self.error.write_log("take dataset...")
                self.take_dataset()

                if self.log.has_log_files():
                    self.error.write_log("has log files...")
                    self.log.post_log_files(self.dataset)
                else:
                    response = self.api.call(self.dataset)
                    if response:
                        self.error.write_log("Dataset posted!")
                    else:
                        self.error.write_log("Dataset posting failed. Statuscode: {0}".format(response))
                        self.is_data_posted = False  # reset is data posted
                        self.error.write_log("log dataset")
                        self.log.insert(self.dataset)  # log dataset
                        # todo: improvement: max 3 attempts before delete
                        while not self.is_data_posted:
                            self.is_data_posted = self.api.call(self.dataset)
                            time.sleep(self.repost_seconds)
                self.error.write_log("wait: {}".format(self.app_wait_time))
                time.sleep(int(self.app_wait_time))
            except Exception as e:
                print(e)
                self.error.write_log(e)


