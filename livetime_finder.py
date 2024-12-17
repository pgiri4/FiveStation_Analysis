import uproot
import numpy as np
import h5py
import re
import click
@click.command()
@click.option('-d', '--data', type=str, help='ex) /data/exp/ARA/2014/unblinded/L1/ARA02/1027/run004434/event004434.root')
@click.option('-s', '--station', type=int)
def get_unix_time_range(data,station):
    """
    Extracts the max - min of the unixTime branch from eventTree in a ROOT file using uproot.

    Args:
        root_file_path (Path): Path to the ROOT file.

    Returns:
        int: Difference between max and min unixTime, or -1 if the branch is not found or empty.
    """
    run = re.search(r'event0(\d+)',data)
    run= run.group(1)
    print(f'run {run}, station {station}')
    try:
        # Open the ROOT file with uproot
        with uproot.open(data) as file:
            # Access the eventTree and the unixTime branch
            tree = file["eventTree"]
            if "event/unixTime" not in tree.keys():
                print(tree.keys())
                print(f"Error: unixTime branch not found in {data}")
                return -1

            # Load the unixTime values as a NumPy array
            unix_times = tree["event/unixTime"].array(library="np")

            # Compute max - min unixTime
            if len(unix_times) > 0:
                print(unix_times.max() , unix_times.min())
                if station == 1:
                   station =100
                hfile = h5py.File(f'/data/ana/ARA/ARA04/scratch/livetime/station_{station}/run_{run}.h5','w')
                hfile.create_dataset('time',data =unix_times.max() - unix_times.min())
                hfile.close()
    except Exception as e:
        print(f"Error processing {data}: {e}")
        return -1

if __name__ == "__main__":
   get_unix_time_range()

