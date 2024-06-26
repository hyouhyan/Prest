#!/bin/bash

echo "export PATH=/Library/Frameworks/Python.framework/Versions/3.9/bin:$PATH" >> ~/.bash_profile

echo "upgrade pip"
python3 -m pip install --upgrade pip
echo "install mediapipe"
python3 -m pip install mediapipe
echo "install opencv"
python3 -m pip install opencv-python
echo "install pyautogui"
python3 -m pip install pyautogui
echo "install playsound"
python3 -m pip install playsound
echo "install kivy"
python3 -m pip install kivy
python3 -m pip install japanize-kivy
