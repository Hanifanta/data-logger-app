# Generating Graphs and CSV for Data Logger UPT ME Amikom
This project involves processing and analyzing CSV files containing electrical data. The data is resampled to a daily frequency and the mean is calculated for the columns 'IA', 'IB', and 'IC'. The maximum and minimum values for these columns are also calculated on a daily basis. The results are saved as new CSV files and visualized in graphs.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
You need to have Python installed on your machine. The project also requires the following Python libraries:
- pandas
- matplotlib
- tkinter

You can install these libraries using pip:
```bash
pip install pandas matplotlib
```

Running the Code
To run the code, navigate to the directory containing the script and run the following command:
```bash
python data_logger.py (For CLI)
python data_logger_gui.py (For GUI)
```

## Code Overview
The main function in the script is generate_graphs_and_csv(). This function does the following:
- Asks the user for the name of the folder containing the CSV files.
- Reads each CSV file into a pandas DataFrame.
- Converts the 'IA', 'IB', and 'IC' columns to numeric.
- Resamples the data to a daily frequency and calculates the mean for the 'IA', 'IB', and 'IC' columns.
- Calculates the daily maximum and minimum values for the 'IA', 'IB', and 'IC' columns.
- Saves the resampled data to a new CSV file.
- Plots the maximum and minimum values for each column and saves the plots as PNG files.

## Built With
- [Python](https://www.python.org/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)

## Authors
- Hanif Al Irsyad