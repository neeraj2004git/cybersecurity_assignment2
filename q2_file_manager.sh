#!/bin/bash

# while true keeps menu running continuously
while true
do
    echo "1.Create File 2.Delete File 3.Create Dir 4.Delete Dir 5.List 6.Exit"

    # read takes user input
    read choice

    # case checks selected option
    case $choice in
        1) 
            # touch creates a new file
            read name; touch "$name" 
            ;;
        2) 
            # rm deletes a file
            read name; rm "$name" 
            ;;
        3) 
            # mkdir creates a directory
            read name; mkdir "$name" 
            ;;
        4) 
            # rm -r removes directory recursively
            read name; rm -r "$name" 
            ;;
        5) 
            # ls lists files in current directory
            ls 
            ;;
        6) 
            # break exits the loop
            break 
            ;;
        *) echo "Invalid" ;;
    esac
done
