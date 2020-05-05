#!/bin/bash
# Check the past two days' data and set the fine adjust accordingly
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
function avg_error {
    echo "$(python3 data-analysis.py < $1 | grep ERROR | sed "s/ERROR \([0-9.-]*\).*/\1/")"
}
LOGF="Data/interrupts.log"
#Find error from yesterday - there's a strangeness in Python's log file naming that means the name is from 2 days ago
LOGF0="$LOGF.$(date -d "2 days ago" -Idate)"
E0=$(avg_error $LOGF0)
#Error from today
E1=$(avg_error $LOGF)
DRIFT=$(echo "$E1 - $E0" | bc)
echo "Yesterday=$E0, Today=$E1, DRIFT=$DRIFT"