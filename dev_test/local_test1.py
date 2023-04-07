import numpy as np
from scipy.fft import fft, ifft, fftfreq
import matplotlib.pyplot as plt

from service.XRF_fitting import Qz, integrated_I
print(Qz)
print(integrated_I)
# #generate a sample signal with a linear trend and periodic sine wave noise
# t = np.linspace(0, 10, 100)
# signal = 2*t + 0.5*np.sin(2*np.pi*0.5*t) + 0.3*np.sin(2*np.pi*1.5*t)
# freq = fft(signal)
# plt.scatter(fftfreq(100, 10/100)[1:20], freq[1:20])
# plt.show()


# apply Fourier transform to the signal
freq = fft(integrated_I)
N = len(Qz)
plt.scatter(fftfreq(N, (Qz[len(Qz)-1] - Qz[0])/N), np.abs(freq))
plt.show()

signal_filtered = np.real(ifft(freq))

fig, ax = plt.subplots(2, 1, figsize=(10, 6))
ax[0].scatter(Qz, integrated_I)
ax[0].set_title('Original Signal')
ax[1].scatter(Qz, signal_filtered)
ax[1].set_title('Filtered Signal')
plt.tight_layout()
plt.show()

'''
# set the frequencies corresponding to the sine waves to zero
print(abs(freq[0:30]))
freq[5:15] = 0 # set the frequency range that corresponds to the first sine wave to zero
freq[15:25] = 0 # set the frequency range that corresponds to the second sine wave to zero

# apply inverse Fourier transform to the modified frequency spectrum
signal_filtered = np.real(ifft(freq))

# plot the original and filtered signals
fig, ax = plt.subplots(2, 1, figsize=(10, 6))
ax[0].plot(t, signal)
ax[0].set_title('Original Signal')
ax[1].plot(t, signal_filtered)
ax[1].set_title('Filtered Signal')
plt.tight_layout()
plt.show()
'''