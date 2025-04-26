import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from ttkthemes import ThemedTk
import os
import pyttsx3
import logging

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

# --- Text-to-Speech setup ---
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# --- Anomaly detection function ---
def detect_anomalies(input_file, temp_thresh, press_thresh, z_thresh):
    try:
        df = pd.read_csv(input_file).reset_index()

        temp_hard = df["temperature"] > temp_thresh
        press_hard = df["pressure"] < press_thresh

        z_temp = ((df["temperature"] - df["temperature"].mean()) / df["temperature"].std()) > z_thresh
        z_press = ((df["pressure"] - df["pressure"].mean()) / df["pressure"].std()) < -z_thresh

        temp_mask = temp_hard & z_temp
        press_mask = press_hard & z_press

        temp_anomalies = df[temp_mask][["index", "temperature"]].copy()
        press_anomalies = df[press_mask][["index", "pressure"]].copy()

        temp_anomalies.rename(columns={"temperature": "value"}, inplace=True)
        press_anomalies.rename(columns={"pressure": "value"}, inplace=True)

        temp_anomalies["sensor"] = "temperature"
        press_anomalies["sensor"] = "pressure"

        anomalies = pd.concat([temp_anomalies, press_anomalies]).sort_values("index")

        output_file = "anomalies.txt"

        with open(output_file, "w") as f:
            if anomalies.empty:
                f.write("")
                speak("No anomalies detected")
                return f"No high-confidence anomalies found. Output saved to '{output_file}'."
            else:
                if not temp_anomalies.empty:
                    speak("Temperature anomaly detected")
                if not press_anomalies.empty:
                    speak("Pressure anomaly detected")
                for _, row in anomalies.iterrows():
                    f.write(f"{int(row['index'])} {row['sensor']} {row['value']:.2f}\n")
                return f"{len(anomalies)} anomalies detected and saved to '{output_file}'."

    except Exception as e:
        return f"Error: {str(e)}"

# --- Plot function ---
def plot_anomalies(input_file, temp_thresh, press_thresh, z_thresh):
    df = pd.read_csv(input_file).reset_index()

    temp_hard = df["temperature"] > temp_thresh
    press_hard = df["pressure"] < press_thresh

    z_temp = ((df["temperature"] - df["temperature"].mean()) / df["temperature"].std()) > z_thresh
    z_press = ((df["pressure"] - df["pressure"].mean()) / df["pressure"].std()) < -z_thresh

    temp_mask = temp_hard & z_temp
    press_mask = press_hard & z_press

    temp_anomalies = df[temp_mask][["index", "temperature"]]
    press_anomalies = df[press_mask][["index", "pressure"]]

    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle("Telemetry Anomaly Detection", fontsize=14, fontweight='bold')

    axs[0].plot(df["index"], df["temperature"], label="Temperature", color="blue")
    axs[0].scatter(temp_anomalies["index"], temp_anomalies["temperature"], color="red", label="Temp Anomalies")
    axs[0].legend()
    axs[0].set_ylabel("Temperature")
    axs[0].grid(True, linestyle="--", alpha=0.4)

    axs[1].plot(df["index"], df["pressure"], label="Pressure", color="green")
    axs[1].scatter(press_anomalies["index"], press_anomalies["pressure"], color="red", label="Pressure Anomalies")
    axs[1].legend()
    axs[1].set_ylabel("Pressure")
    axs[1].set_xlabel("Time Index")
    axs[1].grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- UI Functionality ---
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    file_path_var.set(filename)

def run_detection():
    input_file = file_path_var.get()

    try:
        temp_thresh = float(temp_thresh_entry.get())
        press_thresh = float(press_thresh_entry.get())
        z_thresh = float(z_thresh_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric threshold values.")
        return

    if not input_file:
        messagebox.showerror("Missing File", "Please select a telemetry CSV file.")
        return

    result_msg = detect_anomalies(input_file, temp_thresh, press_thresh, z_thresh)
    result_label.config(text=result_msg)

def run_plot():
    input_file = file_path_var.get()
    try:
        temp_thresh = float(temp_thresh_entry.get())
        press_thresh = float(press_thresh_entry.get())
        z_thresh = float(z_thresh_entry.get())
        plot_anomalies(input_file, temp_thresh, press_thresh, z_thresh)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- UI Setup ---
root = ThemedTk(theme="arc")
root.title("SkySurveil")
root.geometry("600x450")
root.resizable(False, False)
root.configure(bg="#091057")

file_path_var = tk.StringVar()

header_label = tk.Label(root, text="SkySurveil : Telemetry Anomaly Detection", fg="#FFFFFF", font=("Helvetica", 16, "bold"), bg="#091057")
header_label.pack(pady=20)

file_frame = tk.Frame(root, bg="#091057")
file_frame.pack(pady=5)

tk.Label(file_frame, text="Telemetry CSV File:", fg="#FFFFFF", font=("Helvetica", 12), bg="#091057").pack(side="left", padx=5)
tk.Entry(file_frame, textvariable=file_path_var, width=35, font=("Helvetica", 10), relief="flat").pack(side="left", padx=5)
tk.Button(file_frame, text="Browse", command=browse_file, width=15, bg="#8174A0", fg="white", font=("Helvetica", 10, "bold"), relief="flat").pack(side="left", padx=5)

tk.Label(root, text="Temperature Threshold (>°C):", fg="white", font=("Helvetica", 10), bg="#091057").pack(pady=5)
temp_thresh_entry = tk.Entry(root, font=("Helvetica", 10))
temp_thresh_entry.insert(0, "100")
temp_thresh_entry.pack(pady=5)

tk.Label(root, text="Pressure Threshold (<atm):", fg="white", font=("Helvetica", 10), bg="#091057").pack(pady=5)
press_thresh_entry = tk.Entry(root, font=("Helvetica", 10))
press_thresh_entry.insert(0, "0.5")
press_thresh_entry.pack(pady=5)

tk.Label(root, text="Z-score Threshold (σ):", fg="white", font=("Helvetica", 10), bg="#091057").pack(pady=5)
z_thresh_entry = tk.Entry(root, font=("Helvetica", 10))
z_thresh_entry.insert(0, "3")
z_thresh_entry.pack(pady=5)

action_frame = tk.Frame(root, bg="#091057")
action_frame.pack(pady=15)

tk.Button(action_frame, text="Run Detection", command=run_detection, width=20, bg="#874CCC", fg="white", font=("Helvetica", 12, "bold"), relief="flat").pack(side="left", padx=10)
tk.Button(action_frame, text="Plot Anomalies", command=run_plot, width=20, bg="#874CCC", fg="white", font=("Helvetica", 12, "bold"), relief="flat").pack(side="left", padx=10)

result_label = tk.Label(root, text="Results will be shown here.", fg="white", font=("Helvetica", 10), bg="#091057")
result_label.pack(pady=10)

root.mainloop()
