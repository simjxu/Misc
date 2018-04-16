import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
# This script: Plots sinusoid, then applies a digital filter and plots the resulting sinusoid

# Sinusoid settings
amp = 1.2
freq = 12
t = np.arange(0.0, 2.0, 0.01)

# Plot the Sinusoid
s = np.sin(2*np.pi*freq*t)
plt.plot(t, s)

# Create plot settings
plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('Sine Wave')
plt.grid(True)
# plt.savefig("test.jpg")           # Save figure into current folder
plt.show()

""" For Loops
# x = [1, 2, 3, 4, 5, 7, 9]
#
# for a in x:
#     print(a)
''''''
"""