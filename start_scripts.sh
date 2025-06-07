#!/bin/bash

REPO_ROOT=~/Documents/dev/RoboTest

. $REPO_ROOT/venv/bin/activate

python $REPO_ROOT/keyestudio/i2c_oled_ssd1306.py &

python $REPO_ROOT/vision/yolo11_camera/webstreaming.py &

