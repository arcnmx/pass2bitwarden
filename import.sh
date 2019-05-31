#!/bin/bash

echo "Purge your vault first, then press enter to import"
read

find ~/.password-store -maxdepth 1 -mindepth 1 -type d -not -name .archive -not -name .git -not -name .retired -not -name old -not -name tokens -print0 |
	xargs -0 ./pass2bw.py |
	bw import bitwardencsv /dev/stdin
