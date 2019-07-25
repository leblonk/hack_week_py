#! /bin/sh

mkdir ~/logs
cp /home/pi/hack_week_py/run.sh /home/pi/run.sh
sudo chmod 755 /home/pi/run.sh
sudo cp /home/pi/hack_week_py/leddisplay.service /lib/systemd/system/leddisplay.service
sudo chmod 644 /lib/systemd/system/leddisplay.service
sudo systemctl daemon-reload
sudo systemctl enable leddisplay.service
