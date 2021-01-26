CLOCKDIR="/home/pi/Desktop/STC-clock"
DATADIR="$CLOCKDIR/Data"
echo "Clock System Information"
echo
echo "**Loggers in /etc/rc.local"
grep logger /etc/rc.local
echo "**Running logger processes:"
pgrep -fa logger
echo "**Internal IP:"
hostname -I
echo "**External IP"
curl https://ipinfo.io/ip; echo
echo "**NTP chrony tracking stats"
chronyc tracking
echo "**Latest release logs"
tail -n4 $DATADIR/release.log
echo "**Current setting"
cat $DATADIR/setting.txt; echo
echo "**Latest interrupt logs"
cat $DATADIR/interrupts.log | grep ":00:\|:59:" | tail -n5
cat $DATADIR/interrupts.log | python3 $CLOCKDIR/data-analysis.py -f -d10
echo "**Current time"
date
