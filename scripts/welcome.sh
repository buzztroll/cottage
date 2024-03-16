#!/usr/bin/env bash

. /home/bresnaha/Dev/cottage/.venv/bin/activate
sudo  /home/bresnaha/Dev/cottage/.venv/bin/buzz-welcome-lights &
sleep 1
mpg123 /home/bresnaha/robot_welcome.mp3 > /dev/null
wait
