got to home directory and clone the repo
install libs
sudo apt-get install python3-pil python3-pil.imagetk



1. Create a service file
sudo nano /etc/systemd/system/weightdisplay.service


2. Paste the code
[Unit]
Description=Weight Display Fullscreen
After=graphical.target

[Service]
User=pi
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/usr/bin/python3 /home/pi/weightOnPlanets/weight.py
Restart=always

[Install]
WantedBy=graphical.target

3. enable it

sudo systemctl daemon-reload
sudo systemctl enable weightdisplay.service


4. Run it and check
sudo systemctl start weightdisplay.service

5 reboot
sudo reboot

6. To check logs:

journalctl -u weightdisplay.service -f

Note: to get rid of the password warining -  sudo rm /etc/profile.d/sshpwd.sh


_______________________
1. Check if the service is running
Basic status:
systemctl status weightdisplay.service


You’ll see:

active (running) → GOOD

inactive / failed → something’s wrong

Quick “is it running?”:
systemctl is-active weightdisplay.service


Output:

active → running

inactive / failed → not running

✅ 2. Stop the service
sudo systemctl stop weightdisplay.service

✅ 3. Start the service
sudo systemctl start weightdisplay.service

✅ 4. Restart the service
sudo systemctl restart weightdisplay.service


