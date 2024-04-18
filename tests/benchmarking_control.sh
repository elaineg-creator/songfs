#!/bin/bash



# Print the output of the time command
# echo "ruhhhhh $time_output bruhhhh"

# x=1

# while [ $x -le 5 ]
# do
#     # Run the time command and capture its output
#     time_output=$(time (cp -R test_mountpoint/ bruh/) 2>&1  )
#     # Declare an array
#     declare -a ADDR

#     # Read the output of time command into the array
#     while IFS=$'\n' read -r line; do
#         ADDR+=("$line")
#     done <<< "$time_output"

#     # Print each element of the array
#     # for i in "${ADDR[@]}"; do
#     #   echo "$i"
#     # done

#     # Print a specific element from the array this is the real time difference
#     echo "${ADDR[2]}" 

#     unset ADDR
#     sudo rm -rf bruh
# done



#!/bin/bash

# Repeat the block of code five times
for ((i=1; i<=5; i++)); do

    # Run the time command and capture its output
    time_output=$(time (cp -R python_test_dirs/pynotify_test_songs/ bruh/ > /dev/null) 2>&1)

    # Declare an array
    declare -a ADDR

    # Read the output of time command into the array
    while IFS=$'\n' read -r line; do
        ADDR+=("$line")
    done <<< "$time_output"

    # Print each element of the array
    for j in "${ADDR[@]}"; do
        echo "$j"
    done

    # Print a specific element from the array
    echo "Third element: ${ADDR[2]}"
    echo "Third element: ${ADDR[3]}"

    unset ADDR
    sudo rm -rf bruh
done <<< ""
