import streamlit as st  
import wfdb  
import numpy as np  
from scipy.signal import butter, filtfilt, find_peaks  
import matplotlib.pyplot as plt  

def bandpass_filter(sig, lowcut=0.5, highcut=5.0, fs=125):  
    nyq = 0.5 * fs  
    low, high = lowcut / nyq, highcut / nyq  
    b, a = butter(2, [low, high], btype='band')  
    return filtfilt(b, a, sig)  

def compute_rmssd(rr_intervals):  
    diff_rr = np.diff(rr_intervals)  
    return np.sqrt(np.mean(diff_rr**2))  

def compute_pnn50(rr_intervals):  
    diff_rr = np.abs(np.diff(rr_intervals))  
    return np.sum(diff_rr > 0.05) / len(diff_rr) * 100  

def classify_stress(rmssd, pnn50):  
    if rmssd < 0.020 or pnn50 < 3:  
        return "High Stress"  
    elif rmssd < 0.040 or pnn50 < 10:  
        return "Moderate Stress"  
    else:  
        return "Low Stress"  

st.title("Heart Rate Variability (HRV) Stress Estimator")  
st.write("This Streamlit app automatically loads the PhysioNet BIDMC PPG waveform (record: bidmc01) and computes HRV-based stress levels.")  

st.header("1. Loading PhysioNet Dataset")  
st.write("Source: BIDMC PPG and Respiration Dataset on PhysioNet")  

# Load waveform  
record = wfdb.rdrecord('bidmc01', pn_dir='bidmc')  
ppg = record.p_signal[:,0]  
fs = record.fs  

st.success("Successfully loaded PPG waveform: 60,001 samples at 125 Hz.")  

# Filter PPG  
filtered_ppg = bandpass_filter(ppg, 0.5, 5.0, fs)  

st.header("2. Filtered PPG Waveform")  

fig1, ax1 = plt.subplots(figsize=(10,3))  
ax1.plot(filtered_ppg[:1000])  
ax1.set_title("Filtered PPG Signal (First 1000 Samples)")  
st.pyplot(fig1)  

# Peak Detection  
peaks, _ = find_peaks(filtered_ppg, distance=50)  

st.header("3. Peak Detection")  

fig2, ax2 = plt.subplots(figsize=(10,3))  
ax2.plot(filtered_ppg[:1000])  
mask = peaks[peaks < 1000]  
ax2.plot(mask, filtered_ppg[mask], "rx")  
ax2.set_title("Detected Peaks in PPG (First 1000 Samples)")  
st.pyplot(fig2)  

# RR intervals  
rr_intervals = np.diff(peaks) / fs  

st.header("4. RR Intervals")  

fig3, ax3 = plt.subplots(figsize=(10,3))  
ax3.plot(rr_intervals)  
ax3.set_title("RR Interval Series")  
ax3.set_ylabel("Seconds")  
st.pyplot(fig3)  

# HRV Metrics  
rmssd = compute_rmssd(rr_intervals)  
pnn50 = compute_pnn50(rr_intervals)  
stress = classify_stress(rmssd, pnn50)  

st.header("5. HRV Metrics and Stress Level")  

st.write(f"**RMSSD:** {rmssd:.4f} s")  
st.write(f"**pNN50:** {pnn50:.2f}%")  
st.write(f"**Stress Level:** {stress}")  

st.success("Analysis Complete")
