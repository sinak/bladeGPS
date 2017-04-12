#!/bin/sh

/usr/bin/python /home/linux/sdr/usbnetpower/usbnetpower8800.py reboot

killall bladegps
killall python
cd /home/linux/sdr/bladeGPS/
python rsrf-gps.py

