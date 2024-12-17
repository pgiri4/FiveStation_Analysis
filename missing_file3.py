import os
from pathlib import Path
import uproot  # Ensure uproot is installed: pip install uproot
import re

def bad_runs(station):
    st = re.search(r'ARA0(\d+)',station)
    return st 

def return_bad_runs(files):
    with open(files,'r') as file1:

def list_missing_sensor_file_runs(base_dir, ara_dir, years, output_file):
    """
    List run numbers, sizes of event files, and the unixTime range (max - min) 
    for which the corresponding sensor file is missing.

    Args:
        base_dir (str): Base directory (e.g., "/data/exp/ARA").
        ara_dir (str): Fixed part of the directory (e.g., "unblinded/L1/ARA04").
        years (list): List of years to process (e.g., [2018, 2019, 2020, 2021]).
        output_file (str): Path to the output text file for recording missing runs, file sizes, and unixTime range.

    Returns:
        None
    """
    with open(output_file, 'w') as outfile:
        for year in years:
            # Construct the directory for the year
            print(f'working for {year}')
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
                        if not sensor_path.exists():
                            event_path = Path(root) / file
                            file_size = event_path.stat().st_size  # Get file size in bytes

                            # Calculate unixTime range using uproot
                            unix_time_range = get_unix_time_range(event_path)

                            # Write the run number, event file size, and unixTime range to the output file
                            outfile.write(f"{run_num},{file_size},{unix_time_range}\n")


def get_unix_time_range(root_file_path):
    """
    Extracts the max - min of the unixTime branch from eventTree in a ROOT file using uproot.

    Args:
        root_file_path (Path): Path to the ROOT file.

    Returns:
        int: Difference between max and min unixTime, or -1 if the branch is not found or empty.
    """
    try:
        # Open the ROOT file with uproot
        with uproot.open(root_file_path) as file:
            # Access the eventTree and the unixTime branch
            tree = file["eventTree"]
            if "event/unixTime" not in tree.keys():
                print(tree.keys())
                print(f"Error: unixTime branch not found in {root_file_path}")
                return -1

            # Load the unixTime values as a NumPy array
            unix_times = tree["event/unixTime"].array(library="np")

            # Compute max - min unixTime
            if len(unix_times) > 0:
                return int(unix_times.max() - unix_times.min())
            else:
                return -1

    except Exception as e:
        print(f"Error processing {root_file_path}: {e}")
        return -1


# Base directory and fixed path
base_dir = "/data/exp/ARA"
stations = ['ARA01', 'ARA02', 'ARA03', 'ARA04', 'ARA05']
years = range(2012, 2024)  # Years to process

# List missing sensor file runs and their event file sizes for each station
for station in stations:
    print('Processing station:', station)
     
    st = bad_runs(station)
    run_log = f'/data/user/pgiri/software/runlogs/logs/a{st}_log.txt' 
    ara_dir = f"unblinded/L1/{station}"
    output_file = f"{station}_missing_sensor_file_sizes_with_unix_time.txt"  # Output file for this station
    list_missing_sensor_file_runs(base_dir, ara_dir, years, output_file)
    print(f"Missing sensor files and sizes for station {station} written to {output_file}")

