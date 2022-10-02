#!/usr/bin/env python3
# This script contains the function about psd operation
import os
import numpy as np
import pycbc
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
