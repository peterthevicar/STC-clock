#!/bin/bash
# Send email with summary of clock stats
cd /home/pi/Desktop/STC-clock
{
	cat msmtp-headers.txt
	tail -n3 Data/daily-correction.log
	echo ""
	python3 data-analysis.py -f -d10 <Data/interrupts.log
	echo ""
	cat Data/interrupts.log
} | msmtp "$(grep To msmtp-headers.txt | sed "s/To: //")"
