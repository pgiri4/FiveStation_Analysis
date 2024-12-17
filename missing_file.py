import os
from pathlib import Path

def count_missing_sensor_files(base_dir, ara_dir, years):
    """
    Count missing sensor files for event files in the specified directories.

    Args:
        base_dir (str): Base directory (e.g., "/data/exp/ARA").
        ara_dir (str): Fixed part of the directory (e.g., "unblinded/L1/ARA04").
        years (list): List of years to process (e.g., [2018, 2019, 2020, 2021]).

    Returns:
        int: Count of missing sensor files.
    """
    missing_count = 0
    
    for year in years:
        # Construct the directory for the year
        year_dir = Path(base_dir) / str(year) / ara_dir
        
        # Recursively traverse directories under the year
        for root, _, files in os.walk(year_dir):
            for file in files:
                if file.startswith("event0") and file.endswith(".root"):
                    # Extract the run number from the event file name
                    run_num = file.split("event0")[-1].split(".root")[0]
                    sensor_file = f"sensorHk0{run_num}.root"
                    sensor_path = Path(root) / sensor_file
                    
                    # Check if the corresponding sensor file exists
                    if not sensor_path.exists():
                        missing_count += 1
                        #print(f'{run_num}',sensor_path)    
    return missing_count

# Base directory and fixed path
base_dir = "/data/exp/ARA"
#ara_dir = "unblinded/L1/ARA05PA"
stations = ['ARA01','ARA02','ARA03','ARA04','ARA05']
# Years to process
years = range(2012,2024)#[2018, 2019, 2020, 2021]

# Count missing sensor files
for station in stations:
    print('Station : ', station)
    ara_dir =f"unblinded/L1/{station}"
    missing_files_count = count_missing_sensor_files(base_dir, ara_dir, years)
    print(f"Count of missing sensorHk files: {missing_files_count}")

