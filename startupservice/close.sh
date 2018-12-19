#!/bin/bash
sudo ps -fA | grep py  | awk '{print $2}' | sudo xargs kill
fuser -k 5060/udp
fuser -k 9090/udp
fuser -k 20000/udp
fuser -k 19000/udp
echo '****** ports are closed'
sudo systemctl reload asterisk.service
echo '****** poinmt 2'
sudo python /home/sama/Desktop/voiphone/me.py
echo '****** ppoint 3'

