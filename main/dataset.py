from sensorlib.scale import Scale
from sensorlib.dht22 import DHT22
from config.interval_config import IntervalConfig
from config.sensor_config import SensorConfig
from config.audio_config import AudioConfig
import sounddevice as sd
import scipy.io.wavfile
from numpy import diff as np
from numpy import median
import time
from datetime import datetime
from threading import Thread

config_file = '/home/pi/config/config.ini'


class Dataset:
    def __init__(self):
        self.config = IntervalConfig(config_file)
        self.sensor_config = SensorConfig(config_file)
        self.audio_config = AudioConfig(config_file)
        self.dht22_pin = self.sensor_config.dht22["sensor_1"]
        self.dht22 = DHT22(self.dht22_pin)
        self.scale = Scale()

        self.median_interval = 0
        self.wait_time = 0

        self.dataset = {}
        self.temp = []
        self.hum = []
        self.weight = []
        self.fft_data = ""

        self.median_temp = 0
        self.median_hum = 0
        self.median_weight = 0

        self.duration = ""
        self.fs = ""
        self.nWindow = ""

    def get_fft(self):
        self.duration = self.audio_config.get_duration()
        self.fs = self.audio_config.get_fs()
        self.nWindow = 2 ^ 12
        nOverlap = self.nWindow / 2

        try:
            print("recording audio data...")
            audiodata = sd.rec(self.duration * self.fs, samplerate=self.fs, channels=2, dtype='float64')
            sd.wait()
            print("finish recording audio data")
            # do some magic stuff with audio data
        except Exception as e:
            print("something went wrong with the microphone! {0}".format(e))

        return True

    def get_dataset(self):
        fft_thread = Thread(target=self.get_fft)
        fft_thread.start()

        self.median_interval = self.config.get_median_interval()
        self.wait_time = self.config.get_wait_time()

        for i in range(self.median_interval):
            print("take data from sensors...")
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

        now = datetime.now()
        now = now.strftime("%Y-%m-%dT%H:%M:%S")
        fft_thread.join()

        self.dataset = [
            {
                "sourceId": "dht22-temperature-DE-37139-[97834523476534654]",
                "values": [
                    {"ts": str(now), "value": str(self.median_temp)},
                ]
            },
            {
                "sourceId": "dht22-humidity-DE-37139-[97834523476534654]",
                "values": [
                    {"ts": str(now), "value": str(self.median_hum)},
                ]
            },
            {
                "sourceId": "audio-data-DE-37139-[97834523476534654]",
                "values": [
                    {"ts": str(now), "value": self.fft_data}
                ]
            },
            {
                "sourceId": "scale-DE-37139-[97834523476534654]",
                "values": [
                    {"ts": str(now), "value": str(self.median_weight)}
                ]
            }
        ]

        return self.dataset
