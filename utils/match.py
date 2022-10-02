#!/usr/bin/env python3
# This script compute the match and SNR of two signals
# The match is optimised over inclination, azimuth, polarisation angle and time of arrival
import numpy as np
import pycbc
from pycbc.waveform import get_td_waveform

def compute_match(time_series_1, time_series_2, psd, config):
    match = pycbc.filter.matchedfilter.match(time_series_1, time_series_2,
                                             psd=psd, **config)
    squared_opt_snr_1 = pycbc.filter.matchedfilter.sigmasq(time_series_1,
                                                           psd=psd, **config)
    opt_snr_1 = np.sqrt(squared_opt_snr_1)
    squared_opt_snr_2 = pycbc.filter.matchedfilter.sigmasq(time_series_2,
                                                           psd=psd, **config)
    opt_snr_2 = np.sqrt(squared_opt_snr_2)
    return match, opt_snr_1, opt_snr_2
