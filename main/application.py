from api_plugin.sams_science import SamsApi
from config.config import Config
from main.dataset import Dataset
from main.log import Log
from main.error import ErrorLog
import time


class Application:
    def __init__(self):
        self.is_data_posted = False
        self.error = ErrorLog()  # log file to test and debug (writes debug messages)
        self.log = Log()  # sensor data log (if no internet available)
        self.api = SamsApi()  # https://sams.science.itf.llu.lv/ Data Warehouse Plugin to send the data
        self.config = Config()  # Configurations (/config/config.ini)
        self.config_data = self.config.get_config_data()
        self.repost_seconds = int(self.config_data['INTERVAL']['repost_seconds'])
        self.app_wait_time = int(self.config_data['INTERVAL']['app_wait_seconds'])

        self.data = Dataset()  # collect all the data from sensors
        self.dataset = ""

    def take_dataset(self):
        self.dataset = ""
        self.dataset = self.data.get_dataset()

    def start(self):
        while True:
            try:
                self.error.write_log("take dataset...")
                self.take_dataset()
                # if stored data (/log/*.json) available, then try to send this data to the data warehouse
                if self.log.has_log_files():
                    self.error.write_log("has log files...")
                    self.log.post_log_files(self.dataset)
                # if not, take a new dataset to post
                else:
                    response = self.api.call(self.dataset)
                    # try to post data. If api status is 200 then everything is right
                    if response:
                        self.error.write_log("Dataset posted!")
                    # if no internet connection or the api do not allow to send, then store the data
                    # if the status code from api is 500 then the log function will delete the file
                    else:
                        self.error.write_log("Dataset posting failed. Statuscode: {0}".format(response))
                        self.is_data_posted = False  # data where not posted
                        self.error.write_log("log dataset")
                        self.log.insert(self.dataset)  # write new log file with the dataset
                        # todo: improvement: max 3 attempts before delete
                        # try to post every X seconds while the data is not posted (no internet connection
                        while not self.is_data_posted:
                            self.is_data_posted = self.api.call(self.dataset)
                            time.sleep(self.repost_seconds)
                self.error.write_log("wait: {}".format(self.app_wait_time))
                time.sleep(int(self.app_wait_time))  # sleep X seconds before collecting the new data
            except Exception as e:
                print(e)
                self.error.write_log(e)


