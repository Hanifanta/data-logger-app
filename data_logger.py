# Library
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings

# Function
def extract_date_from_filename(filename):
    date_str = filename.split('_')[0]
    return pd.to_datetime(date_str, format='%Y%m%d', errors='coerce')

def generate_graphs_and_csv():
    folder_name = input("Masukkan nama folder: ")
    output_folder_name = f"{folder_name}_Output"
    os.makedirs(output_folder_name, exist_ok=True)  # Membuat folder output
    
    files = [f for f in os.listdir(folder_name) if f.endswith('.csv')]
    
    all_data = {}
    
    for file in files:
        df = pd.read_csv(os.path.join(folder_name, file), parse_dates=['Time Stamp'], index_col='Time Stamp', dtype={'THD V': 'str'})  # Ganti 'Column_Name' dengan nama kolom yang bermasalah
        numeric_cols = ['IA', 'IB', 'IC']
        df = df[numeric_cols]
        df = df.dropna(axis=1, how='all')
        
        # Skip processing if DataFrame is empty
        if df.empty:
            print(f"File {file} is empty or all rows were dropped. Skipping this file.")
            continue
        
        df.index = pd.to_datetime(df.index)  # Ensure index is datetime
        df = df.sort_index()  # Sort the DataFrame by index
        
        date_from_filename = extract_date_from_filename(file)
        if pd.isnull(date_from_filename):
            print(f"Unable to extract date from the file name: {file}. Skipping this file.")
            continue
        
        month = date_from_filename.strftime('%Y-%m')
        if month not in all_data:
            all_data[month] = [df]
        else:
            all_data[month].append(df)

    for month, data_list in all_data.items():
        # Concatenate all DataFrames in the list
        combined_data = pd.concat(data_list)
        combined_data = combined_data.resample('D').agg(['max', 'min'])  # Resample the data to daily frequency
        
        # Sort index by date
        combined_data.sort_index(inplace=True)
        
        fig, axs = plt.subplots(3, figsize=(16, 15))  # Set the height of the figure to 15 inches
        for i, col in enumerate(['IA', 'IB', 'IC']):
            combined_data[col]['max'].plot(ax=axs[i], color='tab:blue', label='Max')
            combined_data[col]['min'].plot(ax=axs[i], color='tab:red', label='Min')
            axs[i].set_title(f'Max and Min values of {col} for {month}')
            axs[i].set_xlabel('')
            axs[i].set_ylabel(f'{col} Value')
            axs[i].grid(True)
            axs[i].legend()
            axs[i].xaxis.set_major_locator(mdates.DayLocator())  # Set penanda untuk setiap hari
            axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format tanggal
            axs[i].tick_params(axis='x', rotation=45)  # Putar label sumbu x untuk keterbacaan yang lebih baik
            axs[i].yaxis.set_major_locator(plt.MultipleLocator(25))  # Set penanda utama sumbu y ke kelipatan 25
        
        plt.tight_layout(pad=3.0)  # Tambahkan jarak antara subplot
        plt.savefig(os.path.join(output_folder_name, f'{month}_graph.png'), dpi=300)  # Simpan gambar di folder output
        plt.close()

        # Simpan data ke file CSV
        combined_data.to_csv(os.path.join(output_folder_name, f'{month}_max_min.csv'))

    print("====================== S  U  C  E  S  S  :) ======================")

# Eksekusi fungsi
generate_graphs_and_csv()
