# Project Title

This project analyzes photoplethysmogram (PPG) signals to compute heart rate variability (HRV) metrics, including RR intervals, RMSSD, and pNN50, by filtering raw signals and detecting heartbeat peaks, and uses these metrics with literature‑based thresholds to estimate physiological stress.

## Biomedical Context

This application is intended for biomedical researchers, clinicians, and developers of health-monitoring wearables. HRV is a widely accepted non-invasive marker of autonomic nervous system balance, making it useful for evaluating physical stress, fatigue, and cardiovascular risk. The app can be applied in digital health contexts such as stress tracking or recovery monitoring.

## Quick Start Instructions

### Opening the Repository in GitHub Codespaces

[Instructions on how to open this repo in GitHub Codespaces]

### Running the Application

[Exact command(s) to run the app/game, e.g., `pip install streamlit` then `streamlit run app.py` or `DISPLAY=:0 love .`]

## Usage Guide

- **Step 1: Load and Filter Signal** Downloads a PPG recording from PhysioNet and applies bandpass filtering to remove noise.
- **Step 2: Peak Detection** Detects heartbeats in the PPG signal and visualizes the detected peaks.
- **Step 3: Calculate RR Intervals** Derives RR intervals from peak timestamps, plots them, and removes outliers.
- **Step 4: Compute HRV Metrics** Calculates RMSSD, SDNN, and pNN50 from cleaned RR intervals.
- **Step 5:Stress Estimation** Uses RMSSD-based thresholds from peer-reviewed literature to determine stress level (High, Moderate, or Low).
- **Step 6: Output Summary Table** Displays a table of final HRV metrics and the corresponding stress level.


## Data Description (optional)

### Data Source

BIDMC PPG and Respiration Dataset from PhysioNet
https://physionet.org/content/bidmc/1.0.0/

Signals used: bidmc01 PPG waveform

Sampling rate: 125 Hz

Duration: 8 minutes (60,001 samples)



## Project Structure

[Description of the project structure and organization]

