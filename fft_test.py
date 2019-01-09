import urllib
import scipy.io.wavfile
from numpy import fft as fft
from scipy import fftpack

rate, audData = scipy.io.wavfile.read("file.wav")
print("rate: ")
print(rate)
print("data: ")
print(audData)

X = fftpack.fft(audData)
freqs = fftpack.fftfreq(len(audData)) * 100
print(freqs)
