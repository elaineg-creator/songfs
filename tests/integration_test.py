import os
import subprocess
import time
import unittest

##############################################################
#                                                            #
#   Brings up SongFS and compares output to filepaths.txt    #
#                                                            #
#                                                            #
##############################################################

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

# Print out contents of FS
# def output_print():
#      with open(filepaths_data, "a") as f:
#             for root, dirs, files in os.walk(mount_point):
#                 for file in files:
#                     full_path = os.path.join(root, file)
#                     rel_path = os.path.relpath(full_path, start=mount_point)
#                     print(f"Found file: {rel_path}")
#                     # Append the relative path of the file to the text file
#                     f.write(rel_path + "\n")

try:
    # Perform operations on the mounted FS
    print("Listing contents of the mount point:")

    # Initialize list of filepaths
    filepaths_data = "tests/filepaths.txt"
    files_data = []

    count = 0
    total = 0

    with open(filepaths_data, "r") as file:
        # Read each line and append it to the file_paths list
        for line in file:
            files_data.append(line.strip())

    print("SCANNED COMPARISON DATA")
    for ln in files_data:
        print("\t" + ln)

    for root, dirs, files in os.walk(mount_point):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, start=mount_point)
            print(f"Found file: {rel_path}")
            total+=1

            if rel_path in files_data:
                # Remove the rel_path from the file_paths list
                files_data.remove(rel_path)
                count+=1
                print("FILE FOUND (" + str(count) + "/" + str(total) + ")")
            else:
                # If rel_path doesn't exist in file_paths, throw an assertion error
                assert False, f"File not found: {rel_path}"

    
    # output = subprocess.check_output(["ls", "-l", mount_point])
    # print(output.decode("utf-8"))
    # check_root(output)
    assert not files_data, "Some files were not found during the scan."
    print("PASSED ALL TESTS (" + str(count) + "/" + str(total) + ")")

finally:
    # Clean up & terminate songfs process
    proc.terminate()
    proc.wait()
