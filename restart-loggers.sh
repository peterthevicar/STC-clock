#!/bin/bash
if [ "$UID" -ne "0" ]; then
	echo "Must run as root"
	exit 1
fi

# Display the loggers and then kill them
echo "Killing current processes"
pgrep -u root -af logger.py
pkill -u root -f logger.py
# Start the loggers again (copied from rc.local)
echo "Starting new processes"
python3 /home/pi/Desktop/STC-clock/interrupt-logger.py &
python3 /home/pi/Desktop/STC-clock/release-logger.py &
# Display the new logger processes
pgrep -u root -af logger.py
