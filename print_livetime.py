import h5py
import numpy as np
import os
import re
def get_info(station):
    you_count = 0
    exclusion_set = []
    exclusion_set1 = []
    exclusion_file = f'/data/user/pgiri/software/FiveStation/scripts/badRunId/ARA0{station}_missing_sensor_file_sizes_with_unix_time.txt'#
    ex_run_log = f'/data/user/pgiri/software/runlogs/logs/a{station}_log.txt'
   
      
    with open(ex_run_log, "r") as f_exclude:
         for line in f_exclude:
                    # Split line using any whitespace as delimiter
              columns = re.split(r"\s+", line.strip())
              if columns and columns[0].isdigit() :
                 exclusion_set1.append(int(columns[0])) 


    with open(exclusion_file, "r") as f_exclude:
         for line in f_exclude:
         #print(
             exclusion_set.append(int((line.split(','))[0]))
# Path to the combined HDF5 file
    if station ==1:
       station = 100
    combined_file = f"/data/ana/ARA/ARA04/scratch/livetime/station_{station}/A{station}_combined_runs.h5"
# List to hold all the time values
    time_values = []
    total_livetime = 0
    bad_run_livetime = 0
    for run in exclusion_set:
        if int(run) in exclusion_set1:
           you_count +=1
# Open the combined HDF5 file
    with h5py.File(combined_file, "r") as f:
        print("Reading data from:", combined_file)
    
    # Loop through all groups (runs) in the file
        for run in f.keys():
            group = f[run]
        #print(run)        
        # Check if 'time' dataset exists in the group
            if "time" in group:
                time_data = group["time"][()]  # Extract scalar time value
                time_values.append(time_data)  # Add to list
                total_livetime +=time_data
                try:
               #print('run', run)
                   if int(run) in exclusion_set1 and int(run) not in exclusion_set:
                      bad_run_livetime += time_data
                except:
                   pass
                   print('error in reading file') 
            else:
                print(f"Warning: 'time' dataset not found in {run}")

# Convert to a NumPy array
    time_values = np.array(time_values)

# Plot the 1D distribution (histogram)
    print('total livetime', total_livetime/(3600*24*365),total_livetime,bad_run_livetime)
    print(bad_run_livetime)
    print('fraction of lifetime with bad_runs ', (bad_run_livetime/total_livetime)*100)
    print('total you count ', you_count,len(exclusion_set1))
    return (bad_run_livetime/total_livetime)*100
collect = []
for st in range(1,6):
    a = get_info(st)
    collect.append(a)
print(collect)
