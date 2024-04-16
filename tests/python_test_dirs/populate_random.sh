#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory> <num_files>"
    exit 1
fi

# Assign arguments to variables
directory="$1"
num_files="$2"

# Check if the specified directory exists
if [ ! -d "$directory" ]; then
    echo "Directory '$directory' does not exist."
    exit 1
fi

# Generate and create random files
for ((i=1; i<=num_files; i++)); do
    # Generate a random file name
    file_name=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 10)
    # Append ".mp3" extension to the file name
    file_name="$file_name.mp3"
    # Create an empty file with the random name in the specified directory
    touch "$directory/$file_name"
    echo "Created file: $directory/$file_name"
done
