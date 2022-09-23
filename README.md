# DRIFT SIM
Distinguishability test of simluated drifted-driftless gravitational-wave (GW) signal pairs

## Simulation
Please run the following to compute the overlap and signal-to-noise ratio (SNR) of a simluated drifted-driftless GW signal pair:
```bash
# Build docker image
make build

# Start docker container
make args="<args>" start

# Remove docker container
make clean
```

## Arguments:
```bash
1. --psd <path to psd file>                      # default: config/config.yaml
2. -H <Hubble constant>                          # default: 67.8 km s$^-1$ Mpc$^-1$
3. -D <Initial luminosity distance (in Mpc)>     # default: 1000 Mpc
4. --plot                                        # default: False
```
## Example
```bash
# Simulate a drifted-driftless GW signal pair with H=67.8 km/s/Mpc, D=1000 Mpc. Visualize the frequency-domain GW pair 
make args="--plot" start

# Simulate a drifted-driftless GW signal pair with H=100 km/s/Mpc, D=4000 Mpc.
make args="-H 100 -D 4000" start
```

## Config
The configs of the initial waveform, target waveform, and match can be adjusted in `config/config.yaml`

## Results
The script generates a .npy file, which contains the following:
```bash
├── Setting information:
│   ├── Initial luminosity distance of the simulated GW signal
│   └── Hubble constant
│
└── Statistics information:
    ├── Overlap of the drifted-driftless signal pair
    ├── SNR of the drifted signal
    └── SNR of the driftless signal
```

## Mathematics
Based on the approximation of Hubble's law $v_H = H_0 d$, we derive an approximated expression of time-dependent cosmological redshift, which is given by:
    $$z(t) = \frac{D_0 H_0}{c} e^{H_0 t}.$$
Hubble drift is the redshift drift due to the expansion of the Universe over time. In the distinguishability test, we investigate whether the Hubble drift is resolvable with signals detected by LISA. The simulated redshifted waveform $h(f)$ in terms of frequency-domain representation of the initial waveform (without redshift) is given by:
    $$h(f) = \int_{-\infty}^{\infty} h_0(t)e^{-H_0t_0}e^{-2\pi if_{0}t/(1 + z)} \mathrm{d}t.$$
The overlap of two simulated GW signals (drifted and driftless signals) is given by:
    $$\langle h|g \rangle = 2 \int_{f_{min}}^{f_{max}} \frac{h^{\*}(f)g(f) + h(f)g^{\*}(f)}{S_n(f)} \mathrm{d}f,$$
where $S_n(f)$ is the one-sided power spectral density (PSD) of the instrumental noise, $f_{min}$ and $f_{max}$ are the lower and higher frequency cutoffs for the detection respectively.

## Authors
[@wyhwong](https://github.com/wyhwong), [@juan.calderonbustillo](https://git.ligo.org/juan.calderonbustillo)
