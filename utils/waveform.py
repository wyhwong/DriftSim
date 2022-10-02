#!/usr/bin/env python3
# This script generate the initial waveform, apply redshift to input waveform, and resample the psd
import bilby.gw.utils as gwutils
import lalsimulation as lalsim
import numpy as np
import pycbc
from bilby.core import utils
from scipy import interpolate
from scipy import constants

class Waveform():
    def __init__(self, config):
        self.config = config
        # Convert waveform parameters
        self.distance_mpc = self.config['distance']
        self.config['m1'] *= utils.solar_mass
        self.config['m2'] *= utils.solar_mass
        self.config['distance'] *= 1e6 * utils.parsec
        self.config['approximant'] = gwutils.lalsim_GetApproximantFromString(config['approximant'])
        # Extract amplitude, time, and phase
        h_plus_lal, h_cross_lal = lalsim.SimInspiralTD(**self.config)
        self.amp = np.sqrt(h_plus_lal.data.data**2+h_cross_lal.data.data**2)
        h_complex = h_plus_lal.data.data-1j*h_cross_lal.data.data
        self.phase = np.angle(h_complex)

    def apply_redshift(self, config, hubble_constant, luminosity_distance, drifted=True):
        # Chop the required signal duration
        target_length = config['length'] * 365. * 24. * 60. * 60. + 0.1
        delta_time = self.config['deltaT']
        target_dt = config['deltaT']
        redshift = hubble_constant * luminosity_distance * 1000. / constants.c
        redshift *= np.exp(target_length * hubble_constant * 3.24078e-20)
        converted_length = int(target_length * 1.00001 / (1 + redshift) / delta_time)
        converted_start = len(self.amp) - converted_length
        amp = self.amp[converted_start:]
        phase = self.phase[converted_start:]
        time = np.arange(len(amp)) * delta_time

        # Construct redshifted signal
        hubble_drift = np.exp(time * hubble_constant * 3.24078e-20)
        if drifted:
            amp = amp / hubble_drift * (self.distance_mpc / luminosity_distance)
            redshift = (hubble_constant * luminosity_distance * 1000. / constants.c) * hubble_drift
        else:
            amp = amp * (self.distance_mpc / luminosity_distance)
            redshift = hubble_constant * luminosity_distance * 1000. / constants.c
        raw_complex_strain = amp * np.exp(-1j*phase)
        time = time * (1 + redshift)

        # Interpolate the signal with uniform time steps
        interpol = interpolate.interp1d(time, raw_complex_strain)
        interpol_time = np.arange(0, target_length, target_dt)
        complex_strain = interpol(interpol_time)
        complex_strain_ts = pycbc.types.TimeSeries(np.real(complex_strain), delta_t=target_dt)
        return complex_strain_ts
