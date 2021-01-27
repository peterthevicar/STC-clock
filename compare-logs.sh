#!/bin/bash
# compare two log files $1 and $2 for trend and fineadjust
if [ ! -r "$2" ]; then
  echo "useage $0 <logfile1> <logfile2>"
  exit 1
fi
 
cat "$1" |
	python3 data-analysis.py -f -d10 |
	grep "TREND\|FINEA\|AVGTC" | tee /tmp/comp.tmp
cat "$2" |
	python3 data-analysis.py -f -d10 |
	grep "TREND\|FINEA\|AVGTC" | tee -a /tmp/comp.tmp

cat /tmp/comp.tmp |
{
	read a T1 b
	read a F1 b
	read a A1 b
	read a T2 b
	read a F2 b
	read a A2 b
	echo "scale=3; print \"SpDpT=\",($T2 - $T1)/($F2 - $F1), \", Temperature diff=\",$A2 - $A1,\"\n\"" | tee | bc
}
