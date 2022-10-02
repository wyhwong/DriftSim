#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt

def plot_fd(frequency_series, labels, psd, filename):
    # Output directory, we create one if it doesn't exist
    check = os.path.isdir(output_dir)
    if not check:
        os.mkdir(output_dir)

    # Frequency domain visualization
    plt.loglog(psd.sample_frequencies, np.sqrt(np.abs(psd)),
               label='$\sqrt{S_n(f)}$', linestyle='dashed')
    for index, _ in enumerate(labels):
        plt.loglog(frequency_series[index].sample_frequencies,
                   np.abs(frequency_series[index]), label=labels[index])
    plt.title('Frequency Domain')
    plt.ylabel('Amplitude spectral density (Hz$^{1/2}$)')
    plt.xlabel('Frequency (Hz)')
    plt.legend()
    plt.savefig(os.path.abspath(filename))
