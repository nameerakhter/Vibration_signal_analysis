<h1 style="color: blue;">CWRU Vibration Signal Explorer</h1>
This simple Streamlit app allows you to explore vibration signal data from the CWRU dataset. The app loads drive-end, fan-end, ball pass acceleration, and RPM data from the specified CWRU dataset folder. You can select a file, visualize information about the selected file, and plot the drive-end (DE) vibration signal.
<br><br>
<hr>
<h3>This is the homescreen you will be greeted with as soon as you launch the app</h3>
<img width="1280" alt="home" src="https://github.com/nameerakhter/Vibration_signal_analysis/assets/120779958/1957b7be-25b6-40a5-881e-f3e27a371bfa">
<h3>As soon as you upload the dataset file you will be greeted with all the information of the data along with options to plot the Time domain and FFT of the data</h3>
<img width="1280" alt="pic1" src="https://github.com/nameerakhter/Vibration_signal_analysis/assets/120779958/60d7482d-a32f-4ce8-8c58-049ce242a0f3">
<h3>You will also be able to divided the data into segments and see the plot of individual segment</h3>
<div style="display: flex; justify-content: space-between;">
    <img width="390" alt="ss2" src="https://github.com/nameerakhter/Vibration_signal_analysis/assets/120779958/babd641e-e667-4dbe-a247-804d7f1e0764">
    <img width="390" alt="ss3" src="https://github.com/nameerakhter/Vibration_signal_analysis/assets/120779958/0c984cda-86fe-4eb5-b690-f9d6b0efa265">
</div>

 <h3>Usage</h3>

1. Ensure you have the required libraries installed. You can install them using:

    ```bash
    pip install numpy os matplotlib scipy streamlit scikit-learn
    ```

2. Run the app with:

    ```bash
    streamlit run app.py
    ```

3. Select a file from the sidebar to display information about the dataset.

4. Adjust the number of samples to plot using the input field in the sidebar.

