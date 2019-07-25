
if [ ! -d /home/pi/hack_week_py ]; then
    cd /home/pi
    sudo git clone https://github.com/leblonk/hack_week_py
    cd hack_week_py
else
    cd /home/pi/hack_week_py
    sudo git pull origin master
fi
GOOGLE_APPLICATION_CREDENTIALS=/home/pi/.ssh/bucket.json sudo -E python /home/pi/hack_week_py/main.py 2>&1 > /home/pi/hack_week_py/out.log
