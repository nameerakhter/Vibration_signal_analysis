import numpy as np 
import os
import matplotlib.pyplot as plt
import scipy.io
import streamlit as st
from sklearn.preprocessing import MinMaxScaler


def load_cwru_data(dataset_folder):
    de_data = {}
    fe_data = {}
    ba_data = {}
    rpm_data = {}

    file_list = os.listdir(dataset_folder)

    for file_name in file_list:
        if file_name.endswith('.mat'):
            file_path = os.path.join(dataset_folder, file_name)
            CWRU_data = scipy.io.loadmat(file_path)

            for key in CWRU_data.keys():
                if key.endswith('_DE_time'):
                    de_data[file_name] = CWRU_data[key]
                elif key.endswith('_FE_time'):
                    fe_data[file_name] = CWRU_data[key]
                elif key.endswith('_BA_time'):
                    ba_data[file_name] = CWRU_data[key]
                elif key.endswith('RPM'):
                    rpm_data[file_name] = CWRU_data[key][0, 0]

    return de_data, fe_data, ba_data, rpm_data

# Streamlit app starts here
st.title("CWRU Vibration Signal Explorer")

# Load CWRU data
dataset_folder = '/IITR/Dataset/CWRU/'
de_data, fe_data, ba_data, rpm_data = load_cwru_data(dataset_folder)

# Select a file from the loaded data in the sidebar
selected_file = st.sidebar.selectbox("Select a file", list(de_data.keys()))
de_time_data = de_data[selected_file]

# Display information about the selected file in the main area
st.write(f"Selected File: {selected_file}")
st.write(f"Drive-End Data Shape: {de_data[selected_file].shape}")
st.write(f"Fan-end Data Shape: {fe_data[selected_file].shape}")
st.write(f"Ball pass accelaration Data Shape: {ba_data[selected_file].shape}")
st.write(f"RPM Value: {rpm_data[selected_file]}")

sampling_rate = 12000  # 12 kHz
duration = 10 

# Plot DE Time Data
time = np.arange(0, duration, 1/sampling_rate)
de_time_data_signal = de_time_data[:len(time)]


# sample_options = {
#     "All Samples": len(de_time_data),
#     "100 Samples": 100,
#     "500 Samples": 500,
#     "1000 Samples": 1000,
#     "1200 Samples": 1200,
#     "2400 Samples": 2400,
#     "5000 Samples": 5000,
#     "10000 Samples": 10000,
# }

# Allow the user to input the number of samples manually
num_samples = st.sidebar.number_input("Enter the number of samples", min_value=0, max_value=len(de_time_data), value=len(de_time_data), step=1, help="Recommended values: 600, 1200, 10000, 12000", placeholder='Specify the desired samples',format="%d")

# Plot DE Time Data with the selected number of samples
time = np.arange(0, num_samples / sampling_rate, 1/sampling_rate)
de_time_data_signal = de_time_data[:num_samples]

def normalize_data(data):
    scaler = MinMaxScaler(feature_range=(-1,1))
    normalized_data = scaler.fit_transform(data.reshape(-1, 1)).flatten()
    return normalized_data

normalized_data = normalize_data(de_time_data_signal)


st.write(f"Normalized plot of the {selected_file} data with {len(normalized_data)} samples")
fig, ax = plt.subplots(figsize=(25, 12))
ax.plot(time, normalized_data, color='firebrick', label='DE Signal')
ax.set_title(f'Vibration Signal vs Time of {selected_file}', fontsize=30)
ax.set_xlabel('Time (seconds)', fontsize=20)
ax.set_ylabel('Amplitude', fontsize=20)
ax.legend(fontsize=15)

st.pyplot(fig)
