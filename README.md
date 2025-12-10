# BME3053C Final Project Group 10

This project analyzes photoplethysmogram (PPG) signals to compute heart rate variability (HRV) metrics, including RR intervals, RMSSD, and pNN50, by filtering raw signals and detecting heartbeat peaks, and uses these metrics with literature‑based thresholds to estimate physiological stress.

## Biomedical Context

This application is intended for biomedical researchers, clinicians, and developers of health-monitoring wearables. HRV is a widely accepted non-invasive marker of autonomic nervous system balance, making it useful for evaluating physical stress, fatigue, and cardiovascular risk. The app can be applied in digital health contexts such as stress tracking or recovery monitoring.

## Quick Start Instructions

### Opening the Repository in GitHub Codespaces
[![Open in Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?template_repository=DevinDaughtry/BME3053C-Final-Project)
1. Navigate to this repository on GitHub.
2. Click the green “Code” button.
3. Select “Open with Codespaces” → “New codespace” on the main branch.
4. Once the Codespace initializes, open the file HRV_Analysis.ipynb.

### Running the Application

1. With the notebook open in Codespaces, click “Run All” or run each cell individually.
2. All required packages are pre-installed in Codespaces.
If running locally, install dependencies first: pip install -r requirements.txt
Then open the notebook using Jupyter: jupyter notebook HRV_Analysis.ipynb
This project is notebook-based — there is no need for streamlit or a separate app runner.

## Usage Guide

- **Step 1: Load and Filter Signal** Downloads a PPG recording from PhysioNet and applies bandpass filtering to remove noise.
- **Step 2: Peak Detection** Detects heartbeats in the PPG signal and visualizes the detected peaks.
- **Step 3: Calculate RR Intervals** Derives RR intervals from peak timestamps, plots them, and removes outliers.
- **Step 4: Compute HRV Metrics** Calculates RMSSD, SDNN, and pNN50 from cleaned RR intervals.
- **Step 5:Stress Estimation** Uses RMSSD-based thresholds from peer-reviewed literature to determine stress level (High, Moderate, or Low).
- **Step 6: Output Summary Table** Displays a table of final HRV metrics and the corresponding stress level.


## Data Description

### Data Source

BIDMC PPG and Respiration Dataset from PhysioNet
https://physionet.org/content/bidmc/1.0.0/

Signals used: bidmc01 PPG waveform

Sampling rate: 125 Hz

Duration: 8 minutes (60,001 samples)



## Project Structure

BME3053C-HRV-Project/
📁 .devcontainer/ # GitHub Codespaces configuration folder.
📄 .gitignore # Specifies files/folders to exclude from version control
📄 HRV_Analysis.ipynb # Main Jupyter notebook
📄 README.md # Project documentation
📄 requirements.txt # List of all Python dependencies needed to run the notebook
