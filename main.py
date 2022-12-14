#!/usr/bin/env python3
import argparse
import logging
import os
import numpy as np
from utils.common import load_base_waveform_params, load_target_waveform_params, load_match_params, check_and_create_dir
from utils.waveform import Waveform
from utils.detection import resample_psd, compute_match
from utils.plot import plot_fd


# ------------------------------------------------------------------------------------------------- #
# This script compute the match and SNR of simulated GW drifted-driftless signal pairs              #
# In the distinguishability test, the settings are the following:                                   #
# The binary systems have the same set of intrinsic parameters                                      #
# Only difference: one waveform is Hubble drifted and one is driftless                              #
# Here the 'driftless' means that the distance of the GW source is assumed unchanged                #
# The Hubble drift means the change in redshift of the GW source due to universal expansion         #
# This Hubble drift increases over time and affects the frequency and amplitude of GW signals       #
# Detector used: LISA, mission lifetime: 4 years
# ------------------------------------------------------------------------------------------------- #


def main(args, output_dir):
    # Setting of the simulated waveform
    hubble_constant = args.hubble
    luminosity_distance = args.distance
    output_path = os.path.abspath(f'{output_dir}/data(H={hubble_constant:.3f},D={luminosity_distance:.3f}).npy')

    logging.info(f"Constructing base waveform...")
    init_waveform = Waveform(load_base_waveform_params())
    logging.info(f"Constructed base waveform, length: {len(init_waveform.amp)}.")

    logging.info(f"Constructing drifted waveform...")
    drifted_ts = init_waveform.apply_redshift(load_target_waveform_params(),
                                              hubble_constant,
                                              luminosity_distance,
                                              drifted=True)
    logging.info(f"Constructed drifted waveform, length: {len(drifted_ts)}.")

    logging.info(f"Constructing driftless waveform...")
    driftless_ts = init_waveform.apply_redshift(load_target_waveform_params(),
                                                hubble_constant,
                                                luminosity_distance,
                                                drifted=False)
    logging.info(f"Constructed driftless waveform, length: {len(driftless_ts)}.")

    drifted_fs = drifted_ts.to_frequencyseries()
    target_df = drifted_fs.sample_frequencies[1] - drifted_fs.sample_frequencies[0]
    lisa_psd = resample_psd(args.psd, target_df)
    logging.info(f"Resampled psd profile, df={target_df}.")

    match, snr_drifted, snr_driftless = compute_match(drifted_ts, driftless_ts,
                                                      lisa_psd, load_match_params())
    logging.info(f"Computed match: match={match}, snr_dr={snr_drifted}, snr_dl={snr_driftless}")

    setting_info = [luminosity_distance, hubble_constant]
    statistics_info = [match, snr_drifted, snr_driftless]
    np.save(output_path, np.array([setting_info, statistics_info], dtype=object))
    logging.info(f"Saved data at {output_path}")

    if args.plot:
        driftless_fs = driftless_ts.to_frequencyseries()
        labels = ["$h_{drifted}(f)$", "$h_{driftless}(f)$"]
        filename = f"{output_dir}/(H={hubble_constant:.3f},D={luminosity_distance:.3f}).pdf"
        plot_fd([drifted_fs, driftless_fs],
                labels, lisa_psd, filename)

if __name__ == "__main__":
    # Setting of parser, inputting parameters
    parser = argparse.ArgumentParser(description="Setting of the distinguishability test")
    parser.add_argument("-D", "--distance", type=float,
                        default=1000., help="Value of the targeted luminosity distance in Mpc")
    parser.add_argument("-H", "--hubble", type=float,
                        default=67.8, help="Value of the targeted Hubble constant")
    parser.add_argument("--psd", type=str,
                        default='config/lisa.txt', help="Path to the psd.txt")
    parser.add_argument("--plot", action="store_true",
                        default=False, help="Option to plot the frequency domain")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Input parameters: {args}")

    # Output directory, we create one if it doesn't exist
    output_dir = os.path.abspath('results')
    exist = check_and_create_dir(output_dir)
    if not exist:
        logging.info(f"Output directory {output_dir} does not exists. Created.")
    main(args, output_dir)
