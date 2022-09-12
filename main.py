# !/usr/bin/env python3

# This script compute the match and SNR of simulated GW drifted-driftless signal pairs
# In the distinguishability test, the settings are the following:
# The binary systems have the same set of intrinsic parameters
# Only difference: one waveform is Hubble drifted and one is driftless
# Here the 'driftless' means that the distance of the GW source is assumed unchanged during the GW emission
# The Hubble drift means the change in redshift of the GW source due to universal expansion
# This Hubble drift increases over time and affects the frequency and amplitude of GW signals
# Detector used: LISA, mission lifetime: 4 years

import argparse
import logging
import numpy as np
import os
import yaml
from utils.waveform import Waveform
from utils.psd import resample_psd
from utils.graph import plot_fd
from utils.match import compute_match

def main(args, output_dir):
    # Setting of the simulated waveform
    hubble_constant = args.hubble
    luminosity_distance = args.distance
    config = yaml.load(open("config/config.yaml", 'r'),
                       Loader=yaml.SafeLoader)
    output_path = os.path.abspath('%s/data(H=%.3f,D=%.3f).npy'%(
                                  output_dir, hubble_constant,
                                  luminosity_distance))

    init_waveform = Waveform(config['base_waveform'])
    logging.info(f"Constructed initial waveform, length: {len(init_waveform.amp)}.")

    drifted_ts = init_waveform.apply_redshift(config['target_waveform'],
                                              hubble_constant,
                                              luminosity_distance,
                                              drifted=True)
    driftless_ts = init_waveform.apply_redshift(config['target_waveform'],
                                                hubble_constant,
                                                luminosity_distance,
                                                drifted=False)
    logging.info(f"Constructed drifted waveform, length: {len(drifted_ts)}.")
    logging.info(f"Constructed drifted waveform, length: {len(driftless_ts)}.")

    drifted_fs = drifted_ts.to_frequencyseries()
    target_df = drifted_fs.sample_frequencies[1] - drifted_fs.sample_frequencies[0]
    lisa_psd = resample_psd(args.psd, target_df)
    logging.info(f"Resampled psd profile, df={target_df}.")

    match, snr_drifted, snr_driftless = compute_match(drifted_ts, driftless_ts,
                                                      lisa_psd, config['match'])
    logging.info(f"Computed match: match={match}, snr_dr={snr_drifted}, snr_dl={snr_driftless}")

    setting_info = [luminosity_distance, hubble_constant]
    statistics_info = [match, snr_drifted, snr_driftless]
    np.save(output_path, [setting_info, statistics_info])
    logging.info(f"Saved data at {output_path}")

    if args.plot:
        driftless_fs = driftless_ts.to_frequencyseries()
        drifted_label = "$h_{drifted}(f)$"
        driftless_label = "$h_{driftless}(f)$"
        filename = "(H=%.3f,D=%.3f).pdf"%(hubble_constant, luminosity_distance)
        plot_fd([drifted_fs, driftless_fs],
                [drifted_label, driftless_label],
                lisa_psd, filename)

if __name__ == "__main__":
    # Setting of parser, inputting parameters
    parser = argparse.ArgumentParser(description = "Compute the match and optimal SNR of drifted and not drifted waveforms with different distance and Hubble Constant.")
    parser.add_argument("-D", "--distance", type=float,
                        default=1000.,
                        help = "Value of the targeted luminosity distance in Mpc")
    parser.add_argument("-H", "--hubble", type=float,
                        default=67.8,
                        help = "Value of the targeted Hubble constant")
    parser.add_argument("--psd", type=str,
                        default='config/lisa.txt',
                        help = "Path to the psd.txt")
    parser.add_argument("--plot", action = "store_true",
                        default=False,
                        help = "Option to plot the frequency domain")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Input parameters: {args}")

    # Output directory, we create one if it doesn't exist
    output_dir = os.path.abspath('results')
    check = os.path.isdir(output_dir)
    if check == False:
        os.mkdir(output_dir)
        logging.info(f"Output directory {output_dir} does not exists. Created.")

    main(args, output_dir)
