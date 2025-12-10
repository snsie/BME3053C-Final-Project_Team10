import streamlit as st
import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

# Title
st.title("Heart Rate Variability (HRV) Stress Estimator")
st.markdown("This Streamlit app automatically loads the PhysioNet BIDMC PPG waveform (`bidmc01`) and computes HRV-based stress levels.")

# -----------------------------------------
# 1. Load the PPG signal from PhysioNet
# -----------------------------------------
st.subheader("1. Loading PhysioNet Dataset")
record_name = 'bidmc01'
pn_dir = 'bidmc'

signals, fields = wfdb.rdsamp(record_name, pn_dir=pn_dir)
ppg_signal = signals[:, 1]
fs = int(fields['fs'])

st.success(f"Loaded {record_name} with {len(ppg_signal)} samples at {fs} Hz.")

# -----------------------------------------
# 2. Filter the PPG signal (Bandpass)
# -----------------------------------------
st.subheader("2. Filtered PPG Waveform")

def bandpass_filter(signal, lowcut, highcut, fs, order=3):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

lowcut = 0.5  # Hz
highcut = 5.0  # Hz

ppg_filtered = bandpass_filter(ppg_signal, lowcut, highcut, fs)

fig1, ax1 = plt.subplots()
ax1.plot(ppg_filtered[:1000], label='Filtered PPG')
ax1.set_title("Filtered PPG Signal (First 1000 Samples)")
ax1.set_xlabel("Sample")
ax1.set_ylabel("Amplitude")
ax1.legend()
st.pyplot(fig1)

# -----------------------------------------
# 3. Detect Peaks
# -----------------------------------------
st.subheader("3. Peak Detection")

peaks, _ = find_peaks(ppg_filtered, distance=int(fs * 0.5), prominence=0.5)

fig2, ax2 = plt.subplots()
ax2.plot(ppg_filtered[:1000], label='Filtered PPG')
ax2.plot(peaks[peaks < 1000], ppg_filtered[peaks[peaks < 1000]], "rx", label='Detected Peaks')
ax2.set_title("Detected Peaks in PPG (First 1000 Samples)")
ax2.set_xlabel("Sample")
ax2.set_ylabel("Amplitude")
ax2.legend()
st.pyplot(fig2)

st.write(f"Total peaks detected: {len(peaks)}")

# -----------------------------------------
# 4. Compute RR Intervals
# -----------------------------------------
st.subheader("4. RR Intervals")

peak_times = peaks / fs  # Convert to seconds
rr_intervals = np.diff(peak_times)  # In seconds

fig3, ax3 = plt.subplots()
ax3.plot(rr_intervals, marker='o', linestyle='-')
ax3.set_title("RR Intervals Over Time")
ax3.set_xlabel("Beat Number")
ax3.set_ylabel("RR Interval (sec)")
st.pyplot(fig3)

# -----------------------------------------
# 5. HRV Metrics and Stress Estimation
# -----------------------------------------
st.subheader("5. HRV Metrics and Stress Level")

# Time-domain HRV metrics
rr_diff = np.diff(rr_intervals)
rmssd = np.sqrt(np.mean(rr_diff**2))
diff_50ms = np.sum(np.abs(rr_diff) > 0.05)
pnn50 = (diff_50ms / len(rr_diff)) * 100

st.write(f"**RMSSD:** {rmssd:.2f} ms")
st.write(f"**pNN50:** {pnn50:.2f} %")

# Threshold-based stress classification
if rmssd < 20 or pnn50 < 3:
    stress_level = "High Stress"
elif rmssd > 40 and pnn50 > 10:
    stress_level = "Low Stress"
else:
    stress_level = "Moderate Stress"

st.success(f"Estimated Stress Level: {stress_level}")
st.markdown("---")
st.info("✅ Analysis Complete")
