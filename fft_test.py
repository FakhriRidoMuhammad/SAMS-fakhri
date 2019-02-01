# import urllib
# import scipy.io.wavfile
# import scipy.signal.welch
#
# from numpy import diff as np
#
# rate, audData = scipy.io.wavfile.read("file.wav")
# print("rate: ")
# print(rate)
# print("data: ")
# print(audData)
#
#
# # die folgenden parameter können gerne auch in der config stehen
# nWindow     = 2^12
# nOverlap    = nWindow/2
# nFFT        = nWindow
#
#
# [Pxx, F]    = scipy.signal.welch(audData,fs=rate,window='hanning',nwindow=nWindow,noverlap=nOverlap,nfft=nFFT,detrend=False, return_onesided=True, scaling='density')
#
# # Es wäre unnötig viel Datenvolumen, den gesammten Frequenzvektor zu übertragen. Startwert und Schrittgröße sollten genügen, um einen Wert des Leistungsdichte-Vektors (Pxx)
# # einer bestimmten Frequenzwert aus F zuzuordnen. Der rest ist redundant.
# Fmin        = F(0)
# Fstepsize   = np.diff(F(0:1))
#
# print(Pxx)
