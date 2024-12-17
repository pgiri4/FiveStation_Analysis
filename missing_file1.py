import os
from pathlib import Path

def list_missing_sensor_file_runs(base_dir, ara_dir, years, output_file):
    """
    List run numbers and sizes of event files for which the corresponding sensor file is missing.

    Args:
        base_dir (str): Base directory (e.g., "/data/exp/ARA").
        ara_dir (str): Fixed part of the directory (e.g., "unblinded/L1/ARA04").
        years (list): List of years to process (e.g., [2018, 2019, 2020, 2021]).
        output_file (str): Path to the output text file for recording missing runs and file sizes.

    Returns:
        None
    """
    with open(output_file, 'w') as outfile:
        for year in years:
            # Construct the directory for the year
            year_dir = Path(base_dir) / str(year) / ara_dir

            # Recursively traverse directories under the year
            for root, _, files in os.walk(year_dir):
                for file in files:
                    if file.startswith("event0") and file.endswith(".root"):
                        # Extract the run number from the event file name
                        run_num = file.split("event0")[-1].split(".root")[0]
                        
                        # Construct the corresponding sensor file path
                        sensor_file = f"sensorHk0{run_num}.root"
                        sensor_path = Path(root) / sensor_file

                        # Check if the sensor file is missing
                        if sensor_path.exists():
                            event_path = Path(root) / file
                            file_size = event_path.stat().st_size  # Get file size in bytes
                            # Write the run number and event file size to the output file
                            outfile.write(f"{run_num},{file_size}\n")

# Base directory and fixed path
base_dir = "/data/exp/ARA"
stations = ['ARA01', 'ARA02', 'ARA03', 'ARA04', 'ARA05']
years = range(2012, 2024)  # Years to process

# List missing sensor file runs and their event file sizes for each station
for station in stations:
    print('Processing station:', station)
    ara_dir = f"blinded/L1/{station}"
    output_file = f"{station}_missing_sensor_file_sizes.txt"  # Output file for this station
    #output_file1 = f"{station}_existing_sensor_file_sizes.txt"
    list_missing_sensor_file_runs(base_dir, ara_dir, years, output_file)

    print(f"Missing sensor files and sizes for station {station} written to {output_file}")

