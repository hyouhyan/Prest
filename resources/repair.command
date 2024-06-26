#!/bin/bash

echo "export PATH=/Library/Frameworks/Python.framework/Versions/3.9/bin:$PATH" >> ~/.bash_profile

echo "upgrade pip"
python3 -m pip install --upgrade pip
echo "uninstall mediapipe"
python3 -m pip uninstall -y mediapipe
echo "uninstall opencv"
python3 -m pip uninstall -y opencv-python
echo "uninstall pyautogui"
python3 -m pip uninstall -y pyautogui
echo "install kivy"
python3 -m pip uninstall -y kivy
python3 -m pip uninstall -y japanize-kivy

bash ./install.command
