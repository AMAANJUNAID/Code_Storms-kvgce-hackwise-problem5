# Code_Storms-kvgce-hackwise-problem5

# Team Name and ID
* Team Name: Code Storms
* Team ID: 25

# Problem Number and Title
* Problem Number: 5
* Problem Title: Spacecraft Telemetry Analyzer🚀

# Instructions to Run the Code

1.  **Ensure you have Python 3.x installed.**
2.  **Install the required dependencies:**
    ```bash
    pip install pandas matplotlib ttkthemes pyttsx3
    ```
3.  **Place the telemetry data file (`telemetry.csv`) in the same directory as the Python script.**
4.  **Run the Python script:**
    ```bash
    python main.py
    ```
    

# Dependencies

The following Python libraries are required:

* pandas🐼
* matplotlib📊
* ttkthemes🎨
* pyttsx3 🗣️

You can install them using pip:

```bash

pip install pandas matplotlib ttkthemes pyttsx3

 ```
# Expected Input and Output
# Input:

A CSV file named telemetry.csv containing spacecraft telemetry data.  The file should contain "temperature" and "pressure" columns.

# Output:

A text file named anomalies.txt in the same directory as the script.

If anomalies are detected, the file will contain lines with the following format:
```bash
<index> <sensor> <value>
```
Where:

```bash
<index> is the index of the anomalous data point.
```
```bash
<sensor> is either "temperature" or "pressure".
```
```bash
<value> is the anomalous temperature or pressure value.
```
* If no anomalies are detected, the file will be empty.

* The program will also provide audio feedback using text-to-speech, indicating whether temperature or pressure anomalies were found. 🔊

* A plot will be displayed showing the temperature and pressure data with the detected anomalies highlighted. 📈
