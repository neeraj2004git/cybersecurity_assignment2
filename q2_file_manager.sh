#!/bin/bash

while true
do
    echo "1.Create File 2.Delete File 3.Create Dir 4.Delete Dir 5.List 6.Exit"
    read choice

    case $choice in
        1) read name; touch "$name" ;;
        2) read name; rm "$name" ;;
        3) read name; mkdir "$name" ;;
        4) read name; rm -r "$name" ;;
        5) ls ;;
        6) break ;;
        *) echo "Invalid" ;;
    esac
done

