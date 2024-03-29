#!/bin/bash
# Send email with summary of clock stats
# Sending email account details and auth are in ~/.msmtprc
cd /home/pi/Desktop/STC-clock
{
	echo "To: linuxiseasier@gmail.com, nigel.sethsmith@gmail.com"
    echo "From: lymingtonclock@gmail.com"
    echo "Subject: Update from Lymington Clock"
	echo "Error, drift and correction"
	cat Data/daily-correction.log | awk -v RS='---\n' 'END { print $0 }'
	echo "Online weather forecast for today and tomorrow"
	tail -n2 Data/weather.log
	echo ""
	echo "Today's log analysis"
	python3 data-analysis.py -f -d10 <Data/interrupts.log
	echo ""
	echo "Today's raw data"
	cat Data/interrupts.log
	echo ""
	echo "Current NTP chronyc tracking information"
	chronyc tracking
} | msmtp --read-recipients
