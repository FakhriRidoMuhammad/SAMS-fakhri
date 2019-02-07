import time
import sounddevice as sd
import scipy.io.wavfile
from sensorlib.scale import Scale
from sensorlib.dht22 import DHT22
from sensorlib.ds1820 import DS18B20
from numpy import median
from threading import Thread
from config.config import Config
from api_plugin.sams_science import SamsApi
from datetime import datetime
from pytz import timezone
from scipy import signal
import numpy as np
import math


class Dataset:
    def __init__(self):
        self.config = Config()
        self.config_data = self.config.get_config_data()
        self.dht22 = DHT22(int(self.config_data['DHT22']['pin']))
        self.scale = Scale()
        self.DS18B20 = DS18B20()
        self.api = SamsApi()

        self.median_interval = 0
        self.wait_time = 0

        self.dataset = []
        self.temp = []
        self.hum = []
        self.weight = []
        self.ds_temp = []
        self.fft_data = ""

        self.median_temp = 0
        self.median_hum = 0
        self.median_weight = 0
        self.median_ds_temp = 0

        self.duration = ""
        self.fs = ""
        self.nWindow = ""

    @staticmethod
    def error_message(device, exception_msg):
        return "something went wrong by collecting the {0} dataset! Error: {1}".format(device, exception_msg)

    @staticmethod
    def get_time():
        fmt = "%Y-%m-%d %H:%M:%S %Z%z"
        now_utc = datetime.now(timezone('UTC'))
        now_pacific = now_utc.astimezone(timezone('US/Pacific'))
        return "2019-01-30T09:15:00Z"

    def get_fft_data(self):
        nWindow = pow(2,12)
        nOverlap = nWindow / 2
        nFFT = nWindow
        self.fs = 48000
        self.duration = 10
        try:
            print("recording audio data...")
            audiodata = sd.rec(self.duration * self.fs, samplerate=self.fs, channels=1, dtype='float64')
            sd.wait()
            data = audiodata.transpose()
            print("finish recording audio data")
            [pxx, F] = scipy.signal.welch(data, fs=self.fs, window='hanning', nperseg=nWindow, noverlap=nOverlap,
                                          nfft=nFFT,
                                          detrend=False, return_onesided=True, scaling='density')
            print("fft finish")

            self.dataset.append(
                {
                    "sourceId": "audiodata-".format(self.api.client_id),
                    "value": [
                        {
                            "ts": self.get_time(),
                            "value": 20*math.log10(abs(pxx).astype(int))
                        },
                    ]
                }
            )

        except Exception as e:
            print(self.error_message("audio", e))

        return True

    def get_ds18b20_data(self):
        sensor_counter = self.DS18B20.device_count()
        try:
            if sensor_counter != 0:
                for x in range(sensor_counter):
                    self.median_ds_temp = []
                    for i in range(self.median_interval):
                        print("take ds18b20 data from sensors...")
                        value = self.DS18B20.tempC(x)
                        if value == 998 or value == 85.0:
                            print("DS18B20 does not work properly...")
                        else:
                            self.ds_temp.append(self.DS18B20.tempC(x))
                            time.sleep(self.wait_time)

                    if len(self.ds_temp) != 0:
                        self.median_ds_temp = median(self.ds_temp)
                        del self.ds_temp[:]
                        self.dataset.append(
                            {
                                "sourceId": "dsb18b20-{0}-{1}".format(x, self.api.client_id),
                                "value": [
                                    {
                                        "ts": self.get_time(),
                                        "value": float(self.median_ds_temp)
                                     },
                                ]
                            }
                        )
                        self.median_ds_temp = ""
        except Exception as e:
            print(self.error_message("ds18b20", e))

    def get_dht22_data(self):
        try:
            for i in range(self.median_interval):
                print("take dht22 data from sensors...")
                dhtdata = self.dht22.get_data()
                self.temp.append(dhtdata['temp'])
                self.hum.append(dhtdata['hum'])
                time.sleep(self.wait_time)

            self.median_temp = median(self.temp)
            self.median_hum = median(self.hum)

            self.dataset.append(
                {
                    "sourceId": "dht22-temperature-{0}".format(self.api.client_id),
                    "values": [
                        {
                            "ts": self.get_time(),
                            "value": float(self.median_temp)
                        },
                    ]
                }
            )
            self.dataset.append(
                {
                    "sourceId": "dht22-humidity-{0}".format(self.api.client_id),
                    "values": [
                        {
                            "ts": self.get_time(),
                            "value": float(self.median_hum)
                        },
                    ]
                }
            )

            del self.temp[:]
            del self.hum[:]
        except Exception as e:
            print(self.error_message("dht22", e))

    def get_scale_data(self):
        try:
            for i in range(self.median_interval):
                print("take data from sensors...")
                self.weight.append(self.scale.get_data())
                time.sleep(self.wait_time)

            self.median_weight = median(self.weight)

            del self.weight[:]
            self.dataset.append(
                {
                    "sourceId": self.api.client_id,
                    "value": [
                        {
                            "ts": self.get_time(),
                            "value": float(self.median_weight)
                        }
                    ]
                }
            )
        except Exception as e:
            print(self.error_message("scale", e))

    def get_dataset(self):
        self.dataset = []
        self.median_interval = int(self.config_data['INTERVAL']['median'])
        self.wait_time = int(self.config_data['INTERVAL']['wait_time_seconds'])
        fft_thread = Thread(target=self.get_fft_data)
        dht22_thread = Thread(target=self.get_dht22_data)
        ds18b20_thread = Thread(target=self.get_ds18b20_data)
        scale_thread = Thread(target=self.get_scale_data)

        fft_thread.start()
        dht22_thread.start()
        ds18b20_thread.start()
        scale_thread.start()

        fft_thread.join()
        dht22_thread.join()
        ds18b20_thread.join()
        scale_thread.join()

        return self.dataset
