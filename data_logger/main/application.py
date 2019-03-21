from data_logger.api_plugin.sams_science import SamsApi
from data_logger.config.config import Config
from data_logger.main.dataset import Dataset
from data_logger.main.log_data import LogData
from data_logger.main.logging import Log
import time


class Application:
    def __init__(self):
        self.is_data_posted = False
        self.log = Log()  # log file to test and debug (writes debug messages)
        self.log_data = LogData()  # sensor data log (if no internet available)
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
                self.log.write_log("take dataset...")
                self.take_dataset()
                if not self.dataset:
                    self.log.write_log("dataset not taken")
                # if stored data (/log/*.json) available, then try to send this data to the data warehouse
                if self.log_data.has_log_files():
                    self.log.write_log("has log files...")
                    self.log_data.post_log_files(self.dataset)
                # if not, take a new dataset to post
                else:
                    response = self.api.call(self.dataset)
                    # try to post data. If api status is 200 then everything is right
                    if response == 200:
                        self.log.write_log("dataset posted!")
                    # if no internet connection or the api do not allow to send, then store the data
                    # if the status code from api is 500 then the log function will delete the file
                    else:
                        self.log.write_log("dataset posting failed. Statuscode: {0}".format(response))
                        self.is_data_posted = False  # data where not posted
                        self.log.write_log("log dataset")
                        self.log_data.insert(self.dataset)  # write new log file with the dataset
                        # try to post every X seconds while the data is not posted (no internet connection)
                        while not self.is_data_posted:
                            self.is_data_posted = self.api.call(self.dataset)
                            time.sleep(self.repost_seconds)
                self.log.write_log("wait: {}".format(self.app_wait_time))
                time.sleep(int(self.app_wait_time))  # sleep X seconds before collecting the new data
            except Exception as e:
                self.log.write_log(e)


