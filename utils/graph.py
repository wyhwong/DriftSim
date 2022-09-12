# !/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt

def plot_fd(frequency_series, labels, psd, filename):
    # Output directory, we create one if it doesn't exist
    output_dir = 'fd_visualization'
    check = os.path.isdir(output_dir)
    if check == False:
        os.mkdir(output_dir)

    # Frequency domain visualization
    plt.loglog(psd.sample_frequencies, np.sqrt(np.abs(psd)),
               label='$\sqrt{S_n(f)}$', linestyle='dashed')
    for i in range(len(labels)):
        plt.loglog(frequency_series[i].sample_frequencies,
                   np.abs(frequency_series[i]), label=labels[i])
    plt.title('Frequency Domain')
    plt.ylabel('Amplitude spectral density (Hz$^{1/2}$)')
    plt.xlabel('Frequency (Hz)')
    plt.legend()
    plt.savefig(os.path.abspath(f"{output_dir}/{filename}"))
