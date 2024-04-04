import os
import subprocess
import time
import unittest

# Define the directory containing the MP3 files
mp3_directory = os.path.abspath("./pyFUSE/rootdir")

# Define the mount point for the FUSE file system
mount_point = os.path.abspath("./pyFUSE/mountdir")

print("Mounting " + mp3_directory + " to " + mount_point)

# Start songfs in the background
proc = subprocess.Popen(["python3", "songfs.py", mp3_directory, mount_point])

# Assume 2sec to initialize songFS
time.sleep(2)

# Parse bash printout of dir contents
def parse_printout(txt):
    output_str = output.decode("utf-8")

    # Do string parsing on bash output
    output_lines = output_str.strip().split("\n")
    actual_directories = [line.split(maxsplit=8)[-1] for line in output_lines[1:]]
    print("Output: " + str(actual_directories))
    return actual_directories

# Check root contents
def check_root(output):
    actual_directories = parse_printout(output)

    expected_root = ['Freddy Fender', 'HONDURAS', 'Jimmy Sturr', 'Selena', 
                     'Taylor Swift', 'The Living Tombstone', 'Unknown Artist', 'john s']


    unittest.TestCase().assertListEqual(sorted(actual_directories), sorted(expected_root))
    print("Root dir PASSED")


try:
    # Perform operations on the mounted FS
    print("Listing contents of the mount point:")
    output = subprocess.check_output(["ls", "-l", mount_point])
    print(output.decode("utf-8"))
    check_root(output)

finally:
    # Clean up & terminate songfs process
    proc.terminate()
    proc.wait()
