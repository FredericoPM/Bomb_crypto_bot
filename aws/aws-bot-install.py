from pyautogui import *
import pyautogui
import time
import keyboard

class Config_AWS:
    #TODO: alterar tecla
    _key_await = '0'

    def _write_command_and_await_for_key(self, command, key):
        pyautogui.write(command, interval=.1)
        pyautogui.press('enter')
        keyboard.wait(key)
        time.sleep(.1)
        keyboard.press('backspace')
        time.sleep(1)

    def _write_and_enter(self, line):
        pyautogui.write(line, interval=.1)
        time.sleep(.1)
        pyautogui.press('enter')
        time.sleep(.1)

    def install_ubunto_vncserver(self):
        print('Next comand: "sudo apt update"')
        keyboard.wait(self._key_await)
        time.sleep(.1)
        keyboard.press('backspace')
        time.sleep(1)
        print('Next comand: "sudo apt install xubuntu-desktop"')
        self._write_command_and_await_for_key('sudo apt update', self._key_await)
        print('Next comand: "sudo apt install tightvncserver"')
        self._write_command_and_await_for_key('sudo apt install xubuntu-desktop', self._key_await)
        print('Next comand: "sudo apt install gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal"')
        self._write_command_and_await_for_key('sudo apt install tightvncserver', self._key_await)
        print('Next comand: "vncserver :1"')
        self._write_command_and_await_for_key('sudo apt install gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal', self._key_await)
        pyautogui.write('vncserver :1', interval=.1)
        pyautogui.press('enter')

    def conf_xstartup(self):
        print('Press ' + self._key_await + ' to start')
        keyboard.wait(self._key_await)
        time.sleep(.1)
        keyboard.press('backspace')
        time.sleep(1)
        self._write_and_enter('#\!/bin/sh')
        pyautogui.press('enter')
        self._write_and_enter('export XKL_XMODMAP_DISABLE=1')
        self._write_and_enter('unset SESSION_MANAGER')
        self._write_and_enter('unset DBUS_SESSION_BUS_ADDRESS')
        pyautogui.press('enter')
        self._write_and_enter('[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup')
        self._write_and_enter('[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources')
        self._write_and_enter('xsetroot -solid grey')
        pyautogui.press('enter')
        self._write_and_enter('vncconfig -iconic &')
        self._write_and_enter('gnome-panel &')
        self._write_and_enter('gnome-settings-daemon &')
        self._write_and_enter('metacity &')
        self._write_and_enter('nautilus &')
        pyautogui.write('gnome-terminal &', interval=.1)
        time.sleep(1)
        print("Pres 'Esc' then ':' then type 'wq' and press enter" )
        print("Afether that press '" + self._key_await + "' to continue")
        keyboard.wait(self._key_await)
        time.sleep(.1)
        keyboard.press('backspace')
        time.sleep(1)
        self._write_command_and_await_for_key('vncserver -kill :1', self._key_await)
        pyautogui.write('vncserver -geometry 1920x1080 :1', interval=.1)
        pyautogui.press('enter')

    def install_libraries_and_vivald(self):
        keyboard.wait(self._key_await)
        time.sleep(.1)
        keyboard.press('backspace')
        time.sleep(1)
        self._write_command_and_await_for_key('sudo apt-get update', self._key_await)
        self._write_command_and_await_for_key('wget -qO- http://repo.vivaldi.com/stable/linux_signing_key.pub | sudo apt-key add -', self._key_await)
        self._write_command_and_await_for_key('sudo add-apt-repository "deb [arch=aarch64,arm64] http://repo.vivaldi.com/stable/deb/ stable main" ', self._key_await)
        self._write_command_and_await_for_key('sudo apt install vivaldi-stable', self._key_await)
        self._write_command_and_await_for_key('sudo apt install python3.8', self._key_await)
        self._write_command_and_await_for_key('sudo apt-get install python3-tk python3-dev', self._key_await)
        self._write_command_and_await_for_key('sudo apt-get install scrot', self._key_await)
        self._write_command_and_await_for_key('sudo apt install python3-pip', self._key_await)
        self._write_command_and_await_for_key('python3 -m pip install pyautogui', self._key_await)
        pyautogui.write('python3 -m pip install opencv-python', interval=.1)
        pyautogui.press('enter')

    def install_vivald(self):
        keyboard.wait(self._key_await)
        time.sleep(.1)
        keyboard.press('backspace')
        time.sleep(1)
        self._write_command_and_await_for_key('wget -qO- http://repo.vivaldi.com/stable/linux_signing_key.pub | sudo apt-key add -', self._key_await)
        self._write_command_and_await_for_key('sudo add-apt-repository "deb [arch=aarch64,arm64] http://repo.vivaldi.com/stable/deb/ stable main" ', self._key_await)
        self._write_command_and_await_for_key('sudo apt install vivaldi-stable', self._key_await)
        

config_bot = Config_AWS()
print("Press f1 to start staling ubunto desktop and vncserver")
keyboard.wait('f1')
config_bot.install_ubunto_vncserver()
print('Pleas type this command: "vim ~/.vnc/xstartup", press i to edit delete every thing in the file')
print("Press f1 to start configuring the vnc connection")
keyboard.wait('f1')
config_bot.conf_xstartup()
print("Press f1 to start installing the python libraries and chrome (this should be done insade the ubunto terminal)")
keyboard.wait('f1')
config_bot.install_libraries_and_vivald()
# config_bot.install_vivald()