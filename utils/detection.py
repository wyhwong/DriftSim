#!/usr/bin/env python3
import os
import numpy as np
import pycbc
from pycbc.waveform import get_td_waveform
from scipy import interpolate


def resample_psd(psd_path, target_df):
    raw_psd = np.genfromtxt(os.path.abspath(psd_path))
    interpol = interpolate.interp1d(np.transpose(raw_psd)[0], np.transpose(raw_psd)[1])
    psd_minf = np.min(np.transpose(raw_psd)[0])
    psd_maxf = np.max(np.transpose(raw_psd)[0])
    interpol_frequency = np.arange(psd_minf, psd_maxf, target_df)
    psd = interpol(interpol_frequency)
    psd = pycbc.types.FrequencySeries(psd, delta_f=target_df)
    return psd


def compute_match(time_series_1, time_series_2, psd, config):
    # Note: the match is optimised over inclination, azimuth, polarisation angle, and arrival time
    match = pycbc.filter.matchedfilter.match(time_series_1, time_series_2,
                                             psd=psd, **config)
    squared_opt_snr_1 = pycbc.filter.matchedfilter.sigmasq(time_series_1,
                                                           psd=psd, **config)
    opt_snr_1 = np.sqrt(squared_opt_snr_1)
    squared_opt_snr_2 = pycbc.filter.matchedfilter.sigmasq(time_series_2,
                                                           psd=psd, **config)
    opt_snr_2 = np.sqrt(squared_opt_snr_2)
    return match, opt_snr_1, opt_snr_2
