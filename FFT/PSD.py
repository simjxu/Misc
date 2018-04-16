import json
from scipy import signal
from pprint import pprint
import numpy
import math
import matplotlib as plt

# Open the json file and save into the variable data
with open('lsm_data_compensation_test.json') as data_file:
    data = json.load(data_file)

# Pull data into an array, then identify how many samples there are
samples = data["waveform"]
numsamples = len(samples)

# Perform Welch's periodogram estimation
Pxx = signal.welch(samples)

# Define Compensation Function
x = [0.331,4000]


# Apply squared Compensation to the PSD
for i in Pxx:
    PSDcomp(i) = Pxx(i)*1/F(x,6767/8192*(i-1))^2

# Calculate RMS


def compensate(x,w)
    return sqrt(((pow(x(2),4)-pow(x(2),2)*w.^2).^2+(pow(x(2),3)*w/x(1)).^2)./((pow(x(2),2)-w.^2).^2+(x(2)*w/x(1)).^2).^2)

pprint(numsamples)