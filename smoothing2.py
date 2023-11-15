import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

# Preprocess the CSV to remove trailing commas
with open('WALKING.csv', 'r') as file:
    lines = file.readlines()
    lines = [line.strip(',\n') + '\n' for line in lines]

with open('WALKING_clean.csv', 'w') as file:
    file.writelines(lines)

# Load the cleaned data
data = pd.read_csv('WALKING_clean.csv')

# Increase the window for smoothing
data['accel_z_smooth'] = data['accel_z'].rolling(window=20).mean()

# Set the threshold and distance for peak detection
threshold = 0.6  # You may need to adjust this based on your data
minimum_distance_between_peaks = 91.5  # Adjust based on expected step frequency

# Find peaks with the specified threshold and distance
peaks, _ = find_peaks(data['accel_z_smooth'], height=threshold, distance=minimum_distance_between_peaks)

# Count the detected steps
number_of_steps = len(peaks)
print(f"Number of steps detected: {number_of_steps}")

# Plot the data and detected steps
plt.figure(figsize=(10, 4))
plt.plot(data['timestamp'], data['accel_z'], label='Raw Z-Acceleration')
plt.plot(data['timestamp'], data['accel_z_smooth'], label='Smoothed Z-Acceleration', color='orange')
plt.scatter(data['timestamp'].iloc[peaks], data['accel_z_smooth'].iloc[peaks], color='red', label='Steps Detected')
plt.legend()
plt.title('Step Detection')
plt.xlabel('Time')
plt.ylabel('Z-Acceleration')
plt.show()

