<h1>CWRU Vibration Signal Explorer</h1>
This simple Streamlit app allows you to explore vibration signal data from the CWRU dataset. The app loads drive-end, fan-end, ball pass acceleration, and RPM data from the specified CWRU dataset folder. You can select a file, visualize information about the selected file, and plot the drive-end (DE) vibration signal.
<br><br>
<hr>
<img width="1280" alt="Git_readme_vibration_sginal_explorer" src="https://github.com/nameerakhter/Vibration_signal_analysis/assets/120779958/d2d1bf88-2554-4116-bb65-f6169ef0eca9">

 
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

