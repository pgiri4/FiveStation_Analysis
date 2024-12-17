import h5py
import os
import glob
import re
# Path where your HDF5 files are stored
input_path = "/data/ana/ARA/ARA04/scratch/livetime/station_4"
output_file = "/data/ana/ARA/ARA04/scratch/livetime/station_4/A4_combined_runs.h5"

# List all HDF5 files in the directory
h5_files = glob.glob(os.path.join(input_path, "run_*.h5"))

# Open the output HDF5 file where all data will be combined
with h5py.File(output_file, "w") as output_h5:
    print(f"Combining files into: {output_file}")
    
    # Loop through each input HDF5 file
    for h5_file in h5_files:
        # Extract run number from the file name
        run = os.path.basename(h5_file).split(".")[0]  # e.g., "run_00000"
        run = re.search(r'run_(\d+)', run)
        run_number = str(int(run.group(1)))
        print(run_number)                
        # Open the input HDF5 file
        with h5py.File(h5_file, "r") as input_h5:
            # Check if 'time' dataset exists in the input file
            if "time" in input_h5:
                time_data = input_h5["time"][()]  # Extract scalar value of 'time'
                
                # Create a group in the output file for this run
                run_group = output_h5.create_group(run_number)
                
                # Add the 'time' dataset to this group
                run_group.create_dataset("time", data=time_data)
                
                print(f"Added {run_number}: time = {time_data}")
            else:
                print(f"Warning: 'time' dataset not found in {h5_file}")

print("All files have been combined successfully!")

