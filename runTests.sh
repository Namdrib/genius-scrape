#!/bin/bash

# Automatically runs all tests in the tests folder against Genius_Scrape.py
# Tests exit cases

# Store test cases that failed
failureList=()

for item in tests/* ;do
# for item in tests/song_* ;do
	# echo $item
	
	flags="-o none"
	# If it is an album, must give the album flag to Genius_Scrape
	if [[ $item = tests/album_* ]] ;then
		# echo $item
		flags+=" -i album"
	fi
	
	cat $item | python3 Genius_Scrape.py $flags >&-
	
	# if it failed, add and inform later
	exitCode=$?
	if [[ $exitCode != 0 ]] ; then
		# echo adding $item to failureList
		failureList+=("$item with exit code $exitCode")
	fi
done

if [ ${#failureList[@]} -eq 0 ]; then
	echo "All tests passed!"
else
	echo Failures:
	printf '%s\n' "${failureList[@]}"
fi
