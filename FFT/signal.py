from pylab import *
import scipy.signal as signal

n = 61
a = signal.firwin(n, cutoff = 0.3, window = "hamming")


print(a)