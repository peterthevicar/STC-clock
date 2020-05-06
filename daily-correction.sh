#!/bin/bash
# Check the past two days' data and set the fine adjust accordingly
# Nigel's algorith
#~ Once per day:
#~ Comment: Compare E1 with fast and slow acceptable error values FAE, SAE and correct the clock’s speed if necessary
#~ o       If E1 is less than FAE then adjust WP with one WPI positive
#~ o       Elsif E1 is greater than SAE then adjust WP with one WPI negative
#~ o       Else do nothing
#~ o       Endif
#~ Comment: Check weight position is within physical boundaries:
#~ o       If WP is less than WPMIN then ALARM
#~ o       Elsif WP is greater than WPMAX then ALARM
#~ o       Else do nothing
#~ o       Endif

# Output current date and time for the log
date
cd /home/pi/Desktop/STC-clock

# these variables are in tenths and ticks
FAE="-5"
SAE="5"
WPI="2"
echo "Maximum fast = $FAE, Maximum slow = $SAE"
function avg_error {
    dec_n="$(python3 data-analysis.py -d5 < $1 | grep ERROR | sed 's/ERROR \([0-9.-]*\).*/\1/')"
    # multiply by 10 and round to get error in tenths of seconds
    awk '{printf "%.0f", $1*10}' <<< "$dec_n"
}
LOGF="Data/interrupts.log"
#Find error from yesterday - there's a strangeness in Python's log file naming that means the name is from 2 days ago
LOGF0="$LOGF.$(date -d "2 days ago" -Idate)"
ERRY=$(avg_error $LOGF0)
#Error from today
ERRT=$(avg_error $LOGF)
DRIFT=$((ERRT - ERRY))
echo "Yesterday=$ERRY, Today=$ERRT, DRIFT=$DRIFT"

if [ $ERRT -gt $SAE -o $ERRT -lt $FAE ]; then
    echo "Adjust FA weight by $WPI ticks"
else
    echo "No adjustment needed"
fi
