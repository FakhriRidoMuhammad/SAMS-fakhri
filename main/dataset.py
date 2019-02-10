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
import datetime
from scipy import signal
import numpy as np


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

        self.median_temp = 0
        self.median_hum = 0
        self.median_weight = 0
        self.median_ds_temp = 0

        self.duration = int(self.config_data['AUDIO']['duration'])

    @staticmethod
    def get_time():
        now = datetime.datetime.utcnow()
        return now.strftime('%Y-%m-%dT%H:%M:%S') + now.strftime('.%f')[:0] + 'Z'

    def error(self, device, error):
        self.dataset.append(
            {
                "sourceId": "{0}-{1}".format(device, self.api.client_id),
                "value": [
                    {
                        "ts": self.get_time(),
                        "value": 0
                    },
                ]
            }
        )
        print("something went wrong by collecting the {0} dataset! Error: {1}".format(device, error))

    def get_fft_data(self):
        n_window = pow(2, 12)
        n_overlap = n_window / 2
        n_fft = n_window
        fs = 48000

        try:
            print("recording audio data...")
            audiodata = sd.rec(self.duration * fs, samplerate=fs, channels=1, dtype='float64')
            sd.wait()
            data = audiodata.transpose()
            print("finish recording audio data")
            [pxx, F] = scipy.signal.welch(data, fs=fs, window='hanning', nperseg=n_window, noverlap=n_overlap,
                                          nfft=n_fft,
                                          detrend=False, return_onesided=True, scaling='density')
            print("fft finish")
            temp_data = np.array(pxx).astype(float)
            data = temp_data.tolist()

            self.dataset.append(
                {
                    "sourceId": "audio-{0}".format(self.api.client_id),
                    "value": [
                        {
                            "ts": self.get_time(),
                            "value": data
                        },
                    ]
                }
            )

        except Exception as e:
            self.error("audio", e)

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
            self.error("ds18b20", e)

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
            self.error("dht22", e)

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
                    "sourceId": "scale-{0}".format(self.api.client_id),
                    "value": [
                        {
                            "ts": self.get_time(),
                            "value": float(self.median_weight)
                        }
                    ]
                }
            )
        except Exception as e:
            self.error("scale", e)

    def get_dataset(self):
        self.dataset = []
        self.median_interval = int(self.config_data['INTERVAL']['median'])
        self.wait_time = int(self.config_data['INTERVAL']['wait_time_seconds'])
        fft_thread = Thread(target=self.get_fft_data)
        dht22_thread = Thread(target=self.get_dht22_data)
        ds18b20_thread = Thread(target=self.get_ds18b20_data)
        scale_thread = Thread(target=self.get_scale_data)

        fft_thread.start()
        ds18b20_thread.start()
        dht22_thread.start()
        scale_thread.start()

        fft_thread.join()
        ds18b20_thread.join()
        dht22_thread.join()
        scale_thread.join()

        print(self.dataset)

        return self.dataset
