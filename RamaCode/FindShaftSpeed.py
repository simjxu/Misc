import copy
import json
import numpy as np
from scipy import integrate
from scipy.signal import detrend
​
import dsp.thinkdsp as dsp
​
​
G2VELOCITY_CONSTANT = 9810
test_profiles = [
    {'machine': 'Stanford Primary Chilled Water', 'data_file': 'primary_chilled_water_l2.json'},
    {'machine': 'SVP Sprint Pump 1', 'data_file': 'sprint_pump_1_l2.json'},
    {'machine': 'SVP Sprint Pump 2', 'data_file': 'sprint_pump_2_l2.json'},
    {'machine': 'Stanford Tower Cooling Water', 'data_file': 'tower_cooling_water_l2.json'},
    {'machine': 'SVP Water Injection Pump 1A', 'data_file': 'water_injection_pump_1a_l2.json'},
    {'machine': 'SVP Water Injection Pump 2A', 'data_file': 'water_injection_pump_2a_l2.json'},
    {'machine': 'SVP Water Injection Pump 2B', 'data_file': 'water_injection_pump_2b_l2.json'},
]
​
​
def get_velocity_waveform(acceleration_waveform_data, sample_rate):
    vb_data = copy.deepcopy(acceleration_waveform_data)
    v = integrate.cumtrapz(vb_data) / sample_rate
    vel_wave = dsp.Wave(
        np.array(v),
        framerate=sample_rate
    )

​
# Unit conversion
for i in range(len(vel_wave.ys)):
    #  g to in/s2
    vel_wave.ys[i] *= G2VELOCITY_CONSTANT
​
vel_wave.ys = detrend(vel_wave.ys, type='constant')
return vel_wave

def find_shaft_speed(spectrum, machine, vibration_type='Acceleration'):
    a = 2
    local_peaks = []

    # Create an array called "local peaks" which gets max peak in every 30 Hz range
    # (0-30, 1-31, 2-32, etc.) This array will be 1601 items long
    for f in range(0, 1600, band_range):
        local_peaks.append(
            spectrum.get_max_peak_of_frequency_range(f, f + band_range)
        )

    peak_frequency_count = {}
    for f, _ in local_peaks:
        peak_frequency_count[f] = 1
        for h in peak_frequency_count.keys():
            # t is quotient, m is remainder of division f and h
            t, m = divmod(f, h)
            if t > 1.0 and m < 0.05 * h:
                peak_frequency_count[h] += 1

    speed = 0
    max_harmonic_count = 0
    for f in peak_frequency_count.keys():
        if peak_frequency_count[f] > max_harmonic_count:
            speed = f
            max_harmonic_count = peak_frequency_count[f]

    print("[%s] Shaft speed for %s is %s with %s harmonics" % (
        vibration_type,
        machine,
        speed,
        max_harmonic_count
    ))

def run_test():
    for test_profile in test_profiles:
        with open('data/' + test_profile['data_file']) as data_file:
            sr = 6664
            data = json.load(data_file)
            signal = data['waveform']
            waveform = get_velocity_waveform(signal, sr)
            spectrum = waveform.make_spectrum()
            find_shaft_speed(spectrum, test_profile['machine'], vibration_type='Velocity')
​
if __name__ == '__main__':
    run_test()