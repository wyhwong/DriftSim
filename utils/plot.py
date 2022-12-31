import os
import numpy as np
import matplotlib.pyplot as plt


def get_base_plot(nrows=1, ncols=1, height=6, width=10, title="", ylabel="", xlabel="", tpad=2.5, lpad=0.1, bpad=0.12, fontsize=12):
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))
    fig.tight_layout(pad=tpad)
    fig.subplots_adjust(left=lpad, bottom=bpad)
    fig.suptitle(title, fontsize=fontsize)
    fig.text(x=0.04, y=0.5, s=ylabel, fontsize=fontsize, rotation="vertical", verticalalignment='center')
    fig.text(x=0.5, y=0.04, s=xlabel, fontsize=fontsize, horizontalalignment='center')
    return fig, axes


def plot_fd(frequency_series, labels, psd, filename):
    _, ax = get_base_plot(title='Frequency Domain',
                          ylabel='Amplitude spectral density (Hz$^{1/2}$)',
                          xlabel='Frequency (Hz)',
                          lpad=0.12)
    ax.loglog(psd.sample_frequencies, np.sqrt(np.abs(psd)),
              label='$\sqrt{S_n(f)}$', linestyle='dashed')
    for index, _ in enumerate(labels):
        ax.loglog(frequency_series[index].sample_frequencies,
                  np.abs(frequency_series[index]), label=labels[index])
    plt.legend()
    plt.savefig(os.path.abspath(filename))
