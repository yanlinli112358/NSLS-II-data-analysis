#filter out noise in XF signal
import matplotlib.pyplot as plt

#1. moving average filter
#2. fourier transform filter

from utils.input_output import get_data
from utils.plot_functions import plot_spec
import numpy as np
import pywt

#1. moving average filter
def moving_average_filter(data, window_size = 5):
    filtered_data = np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    return filtered_data

def wavelet_denoise_filter(data, level = 6, wavelet = 'sym4'):
    threshold = np.std(data[0:10]) ** 2
    print(threshold)
    coeffs = pywt.wavedec(data, wavelet, level)
    coeffs_denoised = [pywt.threshold(coeffs_i, threshold, mode='greater') for coeffs_i in coeffs]
    filtered_data = pywt.waverec(coeffs_denoised, wavelet)
    return filtered_data

def ft_denoise_filter(data, cutoff_freq = 0.008):
    fourier_transform = np.fft.fft(data)
    freq = np.fft.fftfreq(len(data), 10)
    filter_mask = np.abs(freq) < cutoff_freq  # Frequency mask for low-pass filter
    filtered_fourier_transform = fourier_transform * filter_mask
    denoised_signal = np.fft.ifft(filtered_fourier_transform)
    return denoised_signal

#filename = '/Users/rachel/NSLS_II_beamtrips/2024_4_trip_final/XRF_data/s20_ODG_0p5mM_KBr_pH4p5-4e56578a.csv'
filename_I = '/Users/rachel/NSLS_II_beamtrips/2024_4_trip_final/XRF_data/s21_ODG_0p5mM_KI_pH9-8dd3adcb.csv'
filename_Cl = '/Users/rachel/NSLS_II_beamtrips/2024_4_trip_final/XRF_data/s44_ODG_0p5mM_KClO4_pH4p5-69585a52.csv'
low_e = 2200
high_e = 2900
energies = np.linspace(low_e, high_e, (high_e - low_e)// 10 + 1)

qz, I_list = get_data(filename_Cl, low_e, high_e)
I_list_filtered = []
for I in I_list:
    I_filtered = ft_denoise_filter(I)
    I_list_filtered.append(I_filtered)

figure, axs = plt.subplots(3, 6, figsize = (18, 9))
axs_flat = axs.flatten()
for i in range(0, 18):
        ax = axs_flat[i]
        ax.plot(energies, I_list[i])
        ax.plot(energies[5: -5], I_list_filtered[i][5:-5])
        ax.text(energies[-30], max(I_list[i]) * 0.9, s = 'Qz = ' + str(round(qz[i], 4)))

figure.suptitle('denoising with fourier transform')
figure.text(0.5, 0.01, 'energies(eV)', ha='center', va='center')
figure.text(0.01, 0.5, 'XF intensity (counts)', ha='center', va='center', rotation='vertical')
plt.tight_layout()
figure.show()

