#!/bin/bash

if [ $# -ne 1 ]; then
        echo "Error: This script takes exactly one argument."
        echo "The argument should be either 'start' or 'stop'."
        exit
fi

if [ $1 = "start" ]; then
	if [ `id -u` -eq 0 ]
	then
		echo "Please start this script without root privileges!"
		echo "Try again without sudo."
		exit 0
	fi
	echo "Checking for updates."
	git pull
	echo "Starting setting server."
	./server.py &
	echo "Done."
	exit
elif [ $1 = "stop" ] ; then
  echo "stop."

else
	echo "Error, illegal argument. Possible values are: 'stop', 'start'."
	exit
fi
