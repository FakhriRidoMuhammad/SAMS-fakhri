from sensorlib.scale import Scale
from sensorlib.dht22 import DHT22
from config.interval_config import IntervalConfig
from numpy import median
import time


class Dataset:
    def __init__(self):
        self.config = IntervalConfig()
        self.dht22 = DHT22(21)
        self.scale = Scale()
        self.median_interval = 0
        self.wait_time = 0

        self.dataset = {}
        self.temp = []
        self.hum = []
        self.weight = []

        self.median_temp = 0
        self.median_hum = 0
        self.median_weight = 0

    def get_dataset(self):
        self.median_interval = self.config.get_median_interval()
        self.wait_time = self.config.get_wait_time()

        for i in range(self.median_interval):
            dhtdata = self.dht22.get_data()
            self.temp.append(dhtdata['temp'])
            self.hum.append(dhtdata['hum'])
            self.weight.append(self.scale.get_data())
            time.sleep(self.wait_time)

        self.median_temp = median(self.temp)
        self.median_hum = median(self.hum)
        self.median_weight = median(self.weight)

        del self.temp[:]
        del self.hum[:]
        del self.weight[:]

        self.dataset = {"temp": self.median_temp, "hum": self.median_hum, "weight": self.median_weight}

        return self.dataset
