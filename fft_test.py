import urllib
import scipy.io.wavfile
import math
import sounddevice as sd
import scipy.io.wavfile

from scipy import signal
import numpy

nWindow = pow(2, 12)
nOverlap = nWindow / 2
nFFT = nWindow
fs = 48000
duration = 10
try:
    print("recording audio data...")
    audiodata = sd.rec(duration * fs, samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    print(len(audiodata))
    data = audiodata.transpose()
    print("finish recording audio data")
    [Pxx, F] = scipy.signal.welch(data, fs, 'hanning', nWindow, nOverlap, nFFT,
                                  False, True, 'density')
    print("nWindow")
    print(nWindow)
    print("nOverlap")
    print(nOverlap)
    print(Pxx.astype(int))

except Exception as e:
    print(e)
