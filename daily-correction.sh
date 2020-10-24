#!/bin/bash
# Check day's data and set the fine adjust accordingly

# Output current date and time for the log
echo "---"
date
cd /home/pi/Desktop/STC-clock

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

# Process today's log file to find the average error and the trend
AVGER=$(avg_error $LOGF)
TREND=$(trend $LOGF)

# The scale on the fine adjust is only approximate, so we need a factor 
#  which relates seconds/day to ticks on the scale
SPDpT="1.0"

echo -n "AVGER=$AVGER, TREND=$TREND, SPDpT=$SPDpT"

# Correct for the error (AVGER+ TREND/2) and the TREND itself, hence 1.5*TREND, divide by how many seconds/day each tick adjusts
ADJ=$(awk '{printf "%+.0f", (-$1 - 1.5*$2) / $3}' <<< "$AVGER $TREND $SPDpT")
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
