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
echo "---"
date
cd /home/pi/Desktop/STC-clock

#~ # these variables are in tenths and ticks
#~ FAE="-0"
#~ SAE="0"
#~ WPI="1"
#~ echo "Maximum fast = $FAE, Maximum slow = $SAE"
function avg_error {
    dec_n="$(python3 data-analysis.py -f -d10 < $1 | grep AVGER | sed 's/AVGER \([0-9.-]*\).*/\1/')"
    # multiply by 10 and round to get error in tenths of seconds
    awk '{printf "%.0f", $1*10}' <<< "$dec_n"
}
function trend {
    dec_n="$(python3 data-analysis.py -f -d10 < $1 | grep TREND | sed 's/TREND \([0-9.-]*\).*/\1/')"
    # multiply by 10 and round to get error in tenths of seconds
    awk '{printf "%.0f", $1*10}' <<< "$dec_n"
}
LOGF="Data/interrupts.log"

# New way using just today's data (AVGER and TREND)
# To correct we need the error at the end of the day (approx AVGER + TREND/2)
# We then correct for this error and the TREND itself, hence 1.5*TREND
AVGER=$(avg_error $LOGF)
TREND=$(trend $LOGF)
echo -n "AVGER=$AVGER, TREND=$TREND"
ADJ=$(awk '{printf "%+.0f", -$1 - 1.5*$2}' <<< "$AVGER $TREND")
echo ", FINEA=$(cat Data/setting.txt), Adjust: $ADJ"

if [ "$ADJ" -ne "+0" ]; then
  echo $ADJ | python3 motor-control.py
fi
#~ if [ $ERRT -gt $SAE ]; then
    #~ echo "-$WPI ticks"
    #~ echo "-$WPI" | python3 motor-control.py
#~ elif [ $ERRT -lt $FAE ]; then
    #~ echo "+$WPI ticks"
    #~ echo "+$WPI" | python3 motor-control.py
#~ else
    #~ echo "None"
#~ fi
