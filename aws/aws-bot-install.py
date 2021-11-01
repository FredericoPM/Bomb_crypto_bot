from os import error
from numpy import logical_not, minimum
from pyautogui import *
import pyautogui
import time
import keyboard

def write_command_and_await_for_key(command, key):
    pyautogui.write(command, interval=.1)
    pyautogui.press('enter')
    keyboard.wait(key)
    time.sleep(1)

def write_and_enter(line):
    pyautogui.write(line, interval=.1)
    time.sleep(.1)
    pyautogui.press('enter')
    time.sleep(.1)

# keyboard.wait('shift')
# time.sleep(1)
# write_command_and_await_for_key('sudo apt update', 'shift')
# write_command_and_await_for_key('sudo apt install xubuntu-desktop', 'shift')
# write_command_and_await_for_key('sudo apt install tightvncserver', 'shift')
# write_command_and_await_for_key('sudo apt install gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal', 'shift')
# write_command_and_await_for_key('vncserver :1', 'shift')

# # write_and_enter('vim ~/.vnc/xstartup')
# # time.sleep(.5)
# # keyboard.press('i')
# # time.sleep(.5)
# # for i in range(0, 300):
# #     keyboard.press('del')
# #     time.sleep(.05)
# keyboard.wait('shift')
# time.sleep(1)
# write_and_enter('#\!/bin/sh')
# pyautogui.press('enter')
# write_and_enter('export XKL_XMODMAP_DISABLE=1')
# write_and_enter('unset SESSION_MANAGER')
# write_and_enter('unset DBUS_SESSION_BUS_ADDRESS')
# pyautogui.press('enter')
# write_and_enter('[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup')
# write_and_enter('[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources')
# write_and_enter('xsetroot -solid grey')
# pyautogui.press('enter')
# write_and_enter('vncconfig -iconic &')
# write_and_enter('gnome-panel &')
# write_and_enter('gnome-settings-daemon &')
# write_and_enter('metacity &')
# write_and_enter('nautilus &')
# pyautogui.write('gnome-terminal &', interval=.1)
# # time.sleep(1)
# # keyboard.press('esc')
# # time.sleep(.5)
# # keyboard.write(':')
# # time.sleep(.5)
# # pyautogui.write('wq', interval=.1)
# # time.sleep(.5)
# # keyboard.wait('shift')
# # time.sleep(1)
# # keyboard.press('enter')

# keyboard.wait('shift')
# time.sleep(1)
# write_command_and_await_for_key('vncserver -kill :1', 'shift')
# write_command_and_await_for_key('vncserver :1', 'shift')

# keyboard.wait('shift')
# time.sleep(1)
# write_command_and_await_for_key('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb', 'shift')
# write_command_and_await_for_key('sudo apt install ./google-chrome-stable_current_amd64.deb', 'shift')

keyboard.wait('shift')
time.sleep(1)
write_command_and_await_for_key('sudo apt-get update', 'shift')
write_command_and_await_for_key('sudo apt install python3.8', 'shift')
write_command_and_await_for_key('sudo apt-get install python3-tk python3-dev', 'shift')
write_command_and_await_for_key('sudo apt install python3-pip', 'shift')
write_command_and_await_for_key('python3 -m pip install pyautogui', 'shift')
write_command_and_await_for_key('python3 -m pip install opencv-python', 'shift')