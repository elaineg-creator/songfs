#!/bin/bash


for ((i=1; i<=10000; i++)); do


    time_output=$(time (cp -R test_mountpoint/ bruh/ > /dev/null) 2>&1)


    declare -a ADDR
    declare -a values

    while IFS=$'\n' read -r line; do
        ADDR+=("$line")
    done <<< "$time_output"

    # for j in "${ADDR[@]}"; do
    #     echo "$j"

    # done 

        # Set the maximum number of files to copy in each batch
    batch_size=50

    time_pattern=$(echo "$time_output" | grep -oE 'user+\s+[0-9]+m[0-9]+\.[0-9]+s')

    printf "%s" "$time_pattern," >> output.csv 

    echo "userrrrrr  $time_pattern, bruhhhh \n"

    time_pattern=$(echo "$time_output" | grep -oE 'sys+\s+[0-9]+m[0-9]+\.[0-9]+s')
    printf "%s\n" "$time_pattern," >> output.csv 

    
    echo "sysssssss      $time_pattern   . \n"

    unset ADDR
    unset time_pattern

	sudo rm -rf bruh    

    sleep 10


    echo "round $i end \n"
done <<< ""
