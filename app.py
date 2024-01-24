import numpy as np 
import os
import matplotlib.pyplot as plt
import scipy.io
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

# Streamlit app starts here
#reducing the distance between seidebar and the results
st.set_page_config(layout="wide")  
st.title(":blue[CWRU] Vibration Signal Explorer")
st.divider()

uploaded_file = st.sidebar.file_uploader(label="Please upload a file",type='.mat',accept_multiple_files=False,key='file_uploader',disabled=False)

if uploaded_file is not None:
    selected_file = uploaded_file.name

    uploaded_data = scipy.io.loadmat(uploaded_file)
    
    uploaded_de_data = None
    
    for key in uploaded_data.keys():
        if key.endswith('_DE_time'):
            uploaded_de_data = uploaded_data[key]
        elif key.endswith('_FE_time'):
            uploaded_fe_data = uploaded_data[key]
        elif key.endswith('_BA_time'):
            uploaded_ba_data = uploaded_data[key]
        elif key.endswith('RPM'):
            uploaded_rpm_data = uploaded_data[key][0,0]
            break  

    if uploaded_de_data is not None:
        st.write("Uploaded File Information:")
        st.write(f"Drive-End Data Shape: {uploaded_de_data.shape}")
        st.write(f"Fan-End Data Shape: {uploaded_fe_data.shape}")
        st.write(f"Ball pass acceleration Data Shape: {uploaded_ba_data.shape}")
        st.write(f"RPM Data Shape: {uploaded_rpm_data}")
        
        # Define de_time_data for later use
        de_time_data = uploaded_de_data
    else:
        st.warning("Drive-End data not found in the uploaded file.")
else:
    st.warning(" Please upload a file." , icon="⚠️")


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


# Subtracting mean from the normalised data and adding radio buttons to choose the plot between FFT or Time Domain
def normalized_minus_mean(data):
    Normalised=normalized_data- np.mean(normalized_data)

    return Normalised

# Radio button options in sidebar
plot_choice = st.sidebar.radio("Select Plot Type", ["Time Domain Plot", "FFT Plot"])

if plot_choice == "Time Domain Plot":
    normalized_and_mean_subtracted_data = normalized_minus_mean(de_time_data_signal)

    st.divider()
    st.write(f"Normalized plot of the {selected_file} data with {len(normalized_and_mean_subtracted_data)} samples")
    fig, ax = plt.subplots(figsize=(25, 12))
    ax.plot(time, normalized_and_mean_subtracted_data, color='firebrick', label='DE Signal')
    ax.set_title(f'Vibration Signal vs Time of {selected_file}', fontsize=30)
    ax.set_xlabel('Time (seconds)', fontsize=20)
    ax.set_ylabel('Amplitude', fontsize=20)
    ax.legend(fontsize=15)

    st.pyplot(fig)

    

elif plot_choice == "FFT Plot":
    normalized_and_mean_subtracted_data = normalized_minus_mean(de_time_data_signal)

    st.divider()
    st.write(f"FFT plot of the Normalized data of the {selected_file} file")
    fft_result = np.fft.fft(normalized_and_mean_subtracted_data)
    freq = np.fft.fftfreq(len(normalized_and_mean_subtracted_data), d=1/sampling_rate)
    positive_freq_mask = freq >= 1

    fig_fft = go.Figure()
    fig_fft.add_trace(go.Scatter(x=freq[positive_freq_mask], y=np.abs(fft_result[positive_freq_mask]),
                             mode='lines', line=dict(color='red'),
                             text=[f'Amplitude={amp:.3f}<br><br>Frequency={freq:.3f} Hz' for amp, freq in zip(np.abs(fft_result[positive_freq_mask]), freq[positive_freq_mask])],
                             hoverinfo='text'))
    fig_fft.update_layout(height=800, width=1200)
    fig_fft.update_xaxes(title_text='Frequency (Hz)')
    fig_fft.update_yaxes(title_text='Amplitude')
    st.plotly_chart(fig_fft)
