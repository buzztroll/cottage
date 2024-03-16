#!/usr/bin/env bash

. /home/bresnaha/Dev/cottage/.venv/bin/activate
sudo  /home/bresnaha/Dev/cottage/.venv/bin/buzz-alert-lights &
sleep 1
sleep 1
for i in `seq 1 5`; do
    mpg123 /home/bresnaha/Dev/cottage/scripts/intruder.mp3
done
wait
