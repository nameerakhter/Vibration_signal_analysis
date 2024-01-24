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
st.write(f"DE Data Shape: {de_data[selected_file].shape}")
st.write(f"FE Data Shape: {fe_data[selected_file].shape}")
st.write(f"BA Data Shape: {ba_data[selected_file].shape}")
st.write(f"RPM Value: {rpm_data[selected_file]}")

sampling_rate = 12000  # 12 kHz
duration = 10 

# Plot DE Time Data
time = np.arange(0, duration, 1/sampling_rate)
de_time_data_signal = de_time_data[:len(time)]

# Define a list of predefined x-axis limit options
x_axis_limit_options = {
    "Full Range": (0, 10),
    "0 to 0.1 seconds": (0, 0.1),
    "0 to 1 seconds": (0, 1),
    "0 to 5seconds": (0, 5),
}

# Select x-axis limits using a selectbox
selected_x_axis_limits = st.sidebar.selectbox("Select X-axis limits", list(x_axis_limit_options.keys()))

# Retrieve the selected x-axis limits
x_axis_limit_min, x_axis_limit_max = x_axis_limit_options[selected_x_axis_limits]

def normalize_data(data):
    scaler = MinMaxScaler(feature_range=(-1,1))
    normalized_data = scaler.fit_transform(data.reshape(-1, 1)).flatten()
    return normalized_data

normalized_data = normalize_data(de_time_data_signal)


st.write(f"Normalized plot of the {selected_file} data against the specified x-axis limit from {x_axis_limit_min} to {x_axis_limit_max} ")
fig, ax = plt.subplots(figsize=(25, 12))
ax.plot(time, normalized_data, color='firebrick', label='DE Signal')
# ax.set_xlim(0, 0.1)
ax.set_xlim(x_axis_limit_min, x_axis_limit_max)  
ax.set_title(f'Vibration Signal vs Time of {selected_file}', fontsize=30)
ax.set_xlabel('Time (seconds)', fontsize=20)
ax.set_ylabel('Amplitude', fontsize=20)
ax.legend(fontsize=15)

st.pyplot(fig)
