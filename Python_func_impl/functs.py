import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, cheby1, cheby2, ellip, filtfilt

# -------------------- Preprocessing Functions --------------------

def detrend_signal(df, column, window=10):
    return df[column] - df[column].rolling(window=window, min_periods=1).mean()

def smooth_signal(df, column, window_size=5):
    return df[column].rolling(window=window_size, min_periods=1).mean()

def normalize_signal(df, column):
    min_val = df[column].min()
    max_val = df[column].max()
    return (df[column] - min_val) / (max_val - min_val)

def zscore_signal(df, column):
    mean = df[column].mean()
    std = df[column].std()
    return (df[column] - mean) / std

def downsample_df(df, factor):
    return df.iloc[::factor, :].reset_index(drop=True)

def baseline_correction(df, column, baseline_window=50):
    baseline = df[column].rolling(window=baseline_window, min_periods=1).median()
    return df[column] - baseline

# -------------------- Sampling Rate & Filter Functions --------------------

def calculate_sampling_rate(timestamps):
    time_diffs = np.diff(timestamps)
    avg_dt = np.mean(time_diffs)
    return 1.0 / avg_dt

def design_filter(filter_type, filter_design, cutoff, fs, order=4, rp=None, rs=None):
    nyq = 0.5 * fs
    if isinstance(cutoff, (list, tuple, np.ndarray)):
        norm_cutoff = [f / nyq for f in cutoff]
    else:
        norm_cutoff = cutoff / nyq

    if filter_design == 'butter':
        b, a = butter(order, norm_cutoff, btype=filter_type)
    elif filter_design == 'cheby1':
        b, a = cheby1(order, rp, norm_cutoff, btype=filter_type)
    elif filter_design == 'cheby2':
        b, a = cheby2(order, rs, norm_cutoff, btype=filter_type)
    elif filter_design == 'ellip':
        b, a = ellip(order, rp, rs, norm_cutoff, btype=filter_type)
    else:
        raise ValueError("Invalid filter design.")
    return b, a

def apply_filter_to_dataframe(df, filter_type='low', filter_design='butter', cutoff=5, order=4, rp=None, rs=None):
    timestamps = df.iloc[:, 0].values
    sensor_data = df.iloc[:, 1:]
    fs = calculate_sampling_rate(timestamps)
    b, a = design_filter(filter_type, filter_design, cutoff, fs, order, rp, rs)
    filtered_data = sensor_data.apply(lambda col: filtfilt(b, a, col), axis=0)
    return pd.concat([df.iloc[:, [0]], filtered_data], axis=1)

# -------------------- Example Demonstration --------------------

# Generate synthetic data
time = np.linspace(0, 10, 1000)
sensor_signal = np.sin(2 * np.pi * 2 * time) + 0.5 * np.random.randn(1000)
df = pd.DataFrame({
    'Time': time,
    'Sensor1': sensor_signal
})

# Apply transformations
df['Detrended'] = detrend_signal(df, 'Sensor1')
df['Smoothed'] = smooth_signal(df, 'Sensor1')
df['Zscore'] = zscore_signal(df, 'Sensor1')
df['Normalized'] = normalize_signal(df, 'Sensor1')
df['BaselineCorrected'] = baseline_correction(df, 'Sensor1')
downsampled_df = downsample_df(df, 10)

# Apply filters
lowpass_df = apply_filter_to_dataframe(df[['Time', 'Sensor1']], filter_type='low', filter_design='butter', cutoff=5, order=4)
highpass_df = apply_filter_to_dataframe(df[['Time', 'Sensor1']], filter_type='high', filter_design='butter', cutoff=5, order=4)

# Plot results
plt.figure(figsize=(15, 12))

plt.subplot(4, 2, 1)
plt.plot(df['Time'], df['Sensor1'])
plt.title("Original Signal")

plt.subplot(4, 2, 2)
plt.plot(df['Time'], df['Smoothed'])
plt.title("Smoothed Signal")

plt.subplot(4, 2, 3)
plt.plot(df['Time'], df['Zscore'])
plt.title("Z-score Normalized")

plt.subplot(4, 2, 4)
plt.plot(df['Time'], df['Normalized'])
plt.title("Min-Max Normalized")

plt.subplot(4, 2, 5)
plt.plot(df['Time'], df['BaselineCorrected'])
plt.title("Baseline Corrected")

plt.subplot(4, 2, 6)
plt.plot(downsampled_df['Time'], downsampled_df['Sensor1'])
plt.title("Downsampled")

plt.subplot(4, 2, 7)
plt.plot(lowpass_df['Time'], lowpass_df['Sensor1'])
plt.title("Low-pass Filtered")

plt.subplot(4, 2, 8)
plt.plot(highpass_df['Time'], highpass_df['Sensor1'])
plt.title("High-pass Filtered")

plt.tight_layout()
plt.show()
