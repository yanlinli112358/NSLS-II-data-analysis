import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# def gaussian function for fitting
def gaussian(x, A, sig, miu):
    y = A * np.exp(-1 * (x - miu) ** 2 / (2 * sig ** 2))
    return y


# def polynomial background
def bkg(x, *coeffs):
    n = 0
    y = 0
    while n < len(coeffs):
        y += coeffs[n] * x ** n
        n += 1
    return y


# def error processing
def r_square(x, fit_x):
    mean = np.sum(x) / len(x)
    ss_res = np.sum((x - fit_x) ** 2)
    ss_tot = np.sum((x - mean) ** 2)
    r_square = 1 - ss_res / ss_tot
    return r_square


# def sum of peaks and curves
def signal_fit(x, y, num_peaks, bkg_order, peak_centers):
    # transform the function to a function with fixed number of parameters
    s = "def signal_total(x"

    var_n = 0
    while var_n <= (num_peaks * 3 + bkg_order):
        s += ", "
        s += "v" + str(var_n)
        var_n += 1
    s += '): \n'
    s += "    y = bkg(x"
    bkg_n = 0
    while bkg_n <= bkg_order:
        s += ','
        s += 'v' + str(bkg_n)
        bkg_n += 1
    s += ') \n'

    n = 0
    while n < num_peaks:
        s += "    y += gaussian(x "
        s += ','
        s += 'v' + str(bkg_order + 1 + n * 3) + ', v' + str(bkg_order + 2 + n * 3) + ', v' + str(bkg_order + 3 + n * 3)
        s += ')\n'
        n += 1

    s += \
        "    return y"
    print(s)
    exec(s, globals())

    # curve fit the transformed function 'signal_total'
    ##determine initial guess and bounds
    maxy = max(y)
    p0_list = []

    countb = 0
    while countb <= bkg_order:
        p0_list.append(0)
        countb += 1
    countg = 0
    while countg < num_peaks:
        p0_list.append(maxy)
        p0_list.append(100)
        p0_list.append(peak_centers[countg])
        countg += 1

    ##fit
    para, pcov = curve_fit(signal_total, x, y, p0=p0_list)
    bkg_return = para[0: bkg_order + 1]
    gaussian_return = para[bkg_order + 1:]

    # print('background parameters = ' + str(bkg_return))
    # print('gaussian parameters = ' + str(gaussian_return))

    # calculate integrated intensity and error
    A1 = gaussian_return[0]
    sig1 = gaussian_return[1]
    intg_I = A1 * sig1

    A1_err = pcov[bkg_order + 1, bkg_order + 1]
    sig1_err = pcov[bkg_order + 2, bkg_order + 2]
    A1_sig1 = pcov[bkg_order + 1, bkg_order + 2]
    err = np.sqrt(abs(A1_err) / A1 ** 2 + abs(sig1_err) / sig1 ** 2 + 2 / sig1 / A1 * np.sqrt(abs(A1_sig1))) * intg_I

    # plot data
    plt.scatter(x, y)
    # plot fit
    s2 = "fit_y = signal_total(x"
    for p in para:
        s2 += ', '
        s2 += str(p)
    s2 += ')\n'
    s2 += 'plt.plot(x, fit_y)'
    exec(s2, globals(), {'x': x}) #x become local variable??

    return (intg_I, err)
