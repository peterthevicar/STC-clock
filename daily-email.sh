#!/bin/bash
# Send email with summary of clock stats
cd /home/pi/Desktop/STC-clock
{
	cat msmtp-headers.txt
	cat Data/daily-correction.log | awk -v RS='---\n' 'END { print $0 }'
	echo ""
	python3 data-analysis.py -f -d0 <Data/interrupts.log
	echo ""
	cat Data/interrupts.log
} | msmtp "$(grep To msmtp-headers.txt | sed "s/To: //")"
