#!/bin/bash
# Use motor-control.py to adjust the pendulum weight and re-write the settings file with the new value
function usage_error {
    echo "usage: $(basename $0) <+|-><nticks>"
    echo "e.g. +10 makes clock approx 1 second slower per day"
    exit 1
}
if [ -z "$1" ]; then
    usage_error
fi
sign="${1:0:1}"
if [ "$sign" != "+" -a "$sign" != "-" ]; then
    usage_error
fi
nticks="${1:1}"
# Check it's an integer
re='^[0-9]+$' # need to do this to allow all forms of re including spaces
if ! [[ "$nticks" =~ $re ]] ; then
    usage_error
fi
#~ echo "sign: $sign"
#~ echo "$nticks"
read cur_setting </home/pi/Desktop/STC-clock/Data/setting.txt
#~ echo "nticks: $nticks"
echo "before: $cur_setting"
new_setting=$(echo "scale=1; $cur_setting $sign $nticks / 10" | bc)
echo "after: $new_setting"
if [ "$new_setting" != "$cur_setting" ]; then
  echo "move weight"
  echo "$sign$nticks" | python3 motor-control.py
else
  echo "nothing to do"
fi
