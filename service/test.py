import numpy as np
import matplotlib.pyplot as plt

#Generate sample data: Noisy signal
t = np.linspace(2200, 3700, 151)
noise_amplitude = 5
from utils.fit_functions import gaussian
noisy_signal = gaussian(t, 120, 200, 2650) + noise_amplitude * np.random.normal(0, noise_amplitude, 151)

# t = np.linspace(0, 10, 1000)
# f_signal = 5  # Frequency of signal
# signal = np.sin(2 * np.pi * f_signal * t)
# noisy_signal = signal + 0.5 * np.random.randn(len(t))  # Add Gaussian noise

# Compute Fourier Transform
fourier_transform = np.fft.fft(noisy_signal)

# Frequency components
freq = np.fft.fftfreq(len(t), t[1] - t[0])
plt.plot(freq, fourier_transform)
plt.show()

# Plot noisy signal and its Fourier spectrum
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, noisy_signal, label='Noisy Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(freq, np.abs(fourier_transform), label='Fourier Transform')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.legend()

# Apply frequency-domain filtering (low-pass filter)
cutoff_freq = 0.005  # Cutoff frequency for low-pass filter
filter_mask = np.abs(freq) < cutoff_freq  # Frequency mask for low-pass filter
filtered_fourier_transform = fourier_transform * filter_mask

# Inverse Fourier Transform
denoised_signal = np.fft.ifft(filtered_fourier_transform)

# Plot denoised signal and its Fourier spectrum
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, np.real(denoised_signal), label='Denoised Signal')
plt.plot(t, noisy_signal, label = 'noisy signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(freq, np.abs(filtered_fourier_transform), label='Filtered Fourier Transform')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.legend()

plt.show()


