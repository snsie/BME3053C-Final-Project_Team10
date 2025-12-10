import streamlit as st
import numpy as np
import wfdb
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt

# -----------------------
# Bandpass filter function
# -----------------------
def bandpass_filter(signal, lowcut, highcut, fs, order=3):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

# -----------------------
# Plotting functions
# -----------------------
def plot_signal(signal, title, peaks=None):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(signal, label="Filtered PPG")
    if peaks is not None:
        ax.plot(peaks, signal[peaks], "rx", label="Detected Peaks")
    ax.set_title(title)
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")
    ax.legend()
    st.pyplot(fig)

def plot_rr_intervals(rr_intervals):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(rr_intervals, marker='o', markersize=2)
    ax.set_title("RR Intervals Over Time")
    ax.set_xlabel("Beat Number")
    ax.set_ylabel("RR Interval (sec)")
    st.pyplot(fig)

# -----------------------
# HRV Metrics Functions
# -----------------------
def compute_rmssd(rr_intervals):
    diff = np.diff(rr_intervals)
    return np.sqrt(np.mean(diff**2))

def compute_pnn50(rr_intervals):
    diff = np.abs(np.diff(rr_intervals))
    count_50ms = np.sum(diff > 0.05)
    return 100.0 * count_50ms / len(diff)

def classify_stress(rmssd, pnn50):
    if rmssd < 20 or pnn50 < 3:
        return "High Stress"
    elif rmssd > 40 and pnn50 > 10:
        return "Low Stress"
    else:
        return "Moderate Stress"

# -----------------------
# Streamlit UI
# -----------------------
st.title("Heart Rate Variability (HRV) Stress Estimator")
st.markdown("This Streamlit app automatically loads the PhysioNet BIDMC PPG waveform (bidmc01) and computes HRV-based stress levels.")

# Step 1: Load Dataset
st.header("1. Loading PhysioNet Dataset")
record_name = 'bidmc01'
pn_dir = 'bidmc'
signals, fields = wfdb.rdsamp(record_name, pn_dir=pn_dir)
ppg_signal = signals[:, 1]  # PPG is column 1
fs = fields['fs']
st.success(f"Loaded {record_name} with {len(ppg_signal)} samples at {fs} Hz.")

# Step 2: Filter Signal
st.header("2. Filtered PPG Waveform")
lowcut = 0.5
highcut = 5.0
ppg_filtered = bandpass_filter(ppg_signal, lowcut, highcut, fs)
plot_signal(ppg_filtered[:1000], "Filtered PPG Signal (First 1000 Samples)")

# Step 3: Detect Peaks (Full Signal)
st.header("3. Peak Detection")
peaks, _ = find_peaks(ppg_filtered, distance=int(fs * 0.5), prominence=0.05)
plot_signal(ppg_filtered[:1000], "Detected Peaks in PPG (First 1000 Samples)", peaks[peaks < 1000])
st.text(f"Total peaks detected: {len(peaks)}")

# Step 4: Compute RR Intervals
st.header("4. RR Intervals")
peak_times = peaks / fs
rr_intervals = np.diff(peak_times)
plot_rr_intervals(rr_intervals)

# Step 5: HRV Metrics
st.header("5. HRV Metrics and Stress Level")
rmssd = compute_rmssd(rr_intervals)
pnn50 = compute_pnn50(rr_intervals)
stress = classify_stress(rmssd, pnn50)

st.markdown(f"**RMSSD:** {rmssd:.2f} ms")
st.markdown(f"**pNN50:** {pnn50:.2f} %")
st.markdown(f"**Estimated Stress Level:** **{stress}**")
st.success("Analysis Complete")
