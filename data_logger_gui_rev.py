import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import filedialog, ttk

def extract_date_from_filename(filename):
    date_str = filename.split('_')[0]
    return pd.to_datetime(date_str, format='%Y%m%d', errors='coerce')

def generate_mean_graph(folder_name, all_data, output_folder_name, high_mean_threshold=50):
    for month, data_list in all_data.items():
        combined_data = pd.concat(data_list)
        combined_data = combined_data.resample('D').agg('mean')
        combined_data.sort_index(inplace=True)

        fig, axs = plt.subplots(3, figsize=(16, 15))
        plt.subplots_adjust(hspace=0.5, wspace=0.3)  # Adjust vertical and horizontal spacing between subplots
        for i, col in enumerate(['IA', 'IB', 'IC']):
            bars = axs[i].bar(combined_data.index, combined_data[col], color='tab:blue', label='Mean', width=0.8)
            for bar, mean_value in zip(bars, combined_data[col]):
                if mean_value > high_mean_threshold:
                    bar.set_color('tab:orange')
            axs[i].set_title(f'Mean values of {col} for {month}')
            axs[i].set_xlabel('Date')
            axs[i].set_ylabel(f'{col} Value')
            axs[i].grid(True)
            axs[i].legend()
            axs[i].xaxis.set_major_locator(mdates.DayLocator(interval=1))
            axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            axs[i].tick_params(axis='x', rotation=45)
            axs[i].yaxis.set_major_locator(plt.MultipleLocator(25))
            axs[i].set_xlim(combined_data.index[0], combined_data.index[-1])  # Set x-axis limits

        plt.tight_layout(pad=3.0)
        plt.savefig(os.path.join(output_folder_name, f'{month}_mean_graph.png'), dpi=300)
        plt.close()

        # Save mean data to CSV
        csv_filename = os.path.join(output_folder_name, f'{month}_mean_data.csv')
        combined_data.to_csv(csv_filename)

def generate_max_min_graph(folder_name, all_data, output_folder_name):
    for month, data_list in all_data.items():
        combined_data = pd.concat(data_list)
        combined_data = combined_data.resample('D').agg(['max', 'min'])
        combined_data.sort_index(inplace=True)

        fig, axs = plt.subplots(3, figsize=(16, 15))
        plt.subplots_adjust(hspace=0.5, wspace=0.3)  # Adjust vertical and horizontal spacing between subplots
        for i, col in enumerate(['IA', 'IB', 'IC']):
            axs[i].plot(combined_data.index, combined_data[col]['max'], color='tab:green', linestyle='--', label='Max')
            axs[i].plot(combined_data.index, combined_data[col]['min'], color='tab:orange', linestyle='--', label='Min')
            axs[i].set_title(f'Max and Min values of {col} for {month}')
            axs[i].set_xlabel('Date')
            axs[i].set_ylabel(f'{col} Value')
            axs[i].grid(True)
            axs[i].legend()
            axs[i].xaxis.set_major_locator(mdates.DayLocator(interval=1))
            axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            axs[i].tick_params(axis='x', rotation=45)
            axs[i].yaxis.set_major_locator(plt.MultipleLocator(25))
            axs[i].set_xlim(combined_data.index[0], combined_data.index[-1])  # Set x-axis limits

        plt.tight_layout(pad=3.0)
        plt.savefig(os.path.join(output_folder_name, f'{month}_max_min_graph.png'), dpi=300)
        plt.close()

        # Save max-min data to CSV
        csv_filename = os.path.join(output_folder_name, f'{month}_max_min_data.csv')
        combined_data.to_csv(csv_filename)

def generate_graphs_and_csv(folder_name, progressbar, label_progress, text_console, button_select_another):
    output_folder_name = f"{folder_name}_Output"
    os.makedirs(output_folder_name, exist_ok=True)  
    
    files = [f for f in os.listdir(folder_name) if f.endswith('.csv')]
    
    if len(files) == 0:
        text_console.insert(tk.END, "No CSV files found in the selected directory. Please select a directory containing CSV files.\n")
        return

    all_data = {}

    progress_increment = 100 / len(files)
    progress = 0

    for file in files:
        df = pd.read_csv(os.path.join(folder_name, file), parse_dates=['Time Stamp'], index_col='Time Stamp', dtype={'THD V': 'str'})
        numeric_cols = ['IA', 'IB', 'IC']
        df = df[numeric_cols]
        df = df.dropna(axis=1, how='all')

        if df.empty:
            text_console.insert(tk.END, f"File {file} is empty or all rows were dropped. Skipping this file.\n")
            continue

        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        date_from_filename = extract_date_from_filename(file)
        if pd.isnull(date_from_filename):
            text_console.insert(tk.END, f"Unable to extract date from the file name: {file}. Skipping this file.\n")
            continue

        month = date_from_filename.strftime('%Y-%m')
        if month not in all_data:
            all_data[month] = [df]
        else:
            all_data[month].append(df)

        progress += progress_increment
        progressbar['value'] = progress
        progressbar.update()

    generate_mean_graph(folder_name, all_data, output_folder_name)
    generate_max_min_graph(folder_name, all_data, output_folder_name)

    text_console.insert(tk.END, "Graphs and CSV files generated successfully!\n")
    button_select_another.config(state=tk.NORMAL)

def select_folder(root):
    label_greeting = ttk.Label(root, text="Welcome to Graphs and CSV Generator!\nDeveloped by Hanif Al Irsyad", font=("Arial", 16, "bold"), justify='center')
    label_greeting.pack(pady=10)

    label_instruction = ttk.Label(root, text="Please select a folder containing CSV files to proceed.", font=("Arial", 12))
    label_instruction.pack(pady=5)

    button = ttk.Button(root, text="Select Folder", command=lambda: browse_folder(root))
    button.pack(pady=10)

def browse_folder(root):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        root.destroy()
        progress_window = tk.Tk()
        progress_window.title("Generating Graphs and CSV")
        
        progress_frame = ttk.Frame(progress_window)
        progress_frame.pack(pady=10)

        progressbar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=400, mode='determinate')
        progressbar.pack(side=tk.LEFT, padx=10)

        label_progress = ttk.Label(progress_frame, text="Please wait...")
        label_progress.pack(side=tk.LEFT)

        text_console = tk.Text(progress_window, wrap=tk.WORD, height=10)
        text_console.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        button_select_another = ttk.Button(progress_window, text="Select Another Folder", state=tk.DISABLED, command=lambda: select_folder(progress_window))
        button_select_another.pack(pady=10)

        generate_graphs_and_csv(folder_selected, progressbar, label_progress, text_console, button_select_another)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generate Graphs and CSV")
    root.geometry("600x400")
    select_folder(root)
    root.mainloop()
