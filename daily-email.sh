#!/bin/bash
# Send email with summary of clock stats
cd /home/pi/Desktop/STC-clock
{
	cat msmtp-headers.txt
	echo "Error, drift and correction"
	cat Data/daily-correction.log | awk -v RS='---\n' 'END { print $0 }'
	echo ""
	echo "Online weather forecast for today and tomorrow"
	tail -n2 Data/weather.txt
	echo ""
	echo "Today's log analysis"
	python3 data-analysis.py -f -d0 <Data/interrupts.log
	echo ""
	echo "Today's raw data"
	cat Data/interrupts.log
} | msmtp "$(grep To msmtp-headers.txt | sed "s/To: //")"
