import time
import random
import pyautogui
from .bot import Bot
from .utils import Utils
from pyautogui import *

class Multi_bot:
    _bot = None
    _windows = []
    _data = None
    _utils = None
    _bot_log = None
    _minimum_time = None
    _small_time = None
    _medium_time = None
    _big_time = None

    def __init__(self, data, log, minimum_time, small_time, medium_time, big_time, utils, navigator_path):
        self._bot = Bot(data, log, minimum_time, small_time, medium_time, big_time, utils)
        self._utils = utils
        self._data = data
        self._bot_log = log
        self._minimum_time = minimum_time
        self._small_time = small_time
        self._medium_time = medium_time
        self._big_time = big_time
        count = 0
        while len(list(filter(lambda e : e != None, self._windows))) != self._data['number_of_bots']:
            if(self._utils.await_for_image("./images/find_screen.png", await_time = 3) != None):
                self._windows.insert(0,
                    {
                        "id": count,
                        "state": 0,
                        "start_time": None
                    }
                )
            else:
                self._windows.insert(0,None)
            count += 1
            if(len(list(filter(lambda e : e != None, self._windows))) != self._data['number_of_bots']):
                pyautogui.keyDown('alt')
                for i in range(0, count):
                    pyautogui.press('tab')
                pyautogui.keyUp('alt')

    def index_of(self, vet, condition):
        count = 0
        for element in vet:
            if(condition(element)):
                return count
            count+=1
        return -1

    def switch_to_windown(self, index):
        pyautogui.keyDown('alt')
        for i in range(0, index):
            pyautogui.press('tab')
        pyautogui.keyUp('alt')
        self._windows.insert(0, self._windows.pop(index))


    def _put_all_to_work(self):
        checked = []
        while len(checked) != self._data['number_of_bots']:
            index = self.index_of(self._windows, lambda e : e != None and e['id'] not in checked)
            self._bot_log.info(f"Starting workflow on bot {self._windows[index]['id']}")
            print(self._windows[index])
            checked.append(self._windows[index]['id'])
            self.switch_to_windown(index)
            index = 0
            while(self._windows[index]['state'] != 3):
                self._windows[index]['state'] = self._bot.select_wat_to_do(self._windows[index]['state'])
                try:
                    if(self._windows[index]['state'] == 1):
                        self._bot.refresh()
                        self._utils.await_for_image("./images/connect-wallet-button.png", await_time = self._big_time, tag = "CONNECT")
                        self._bot.try_to_login()
                    elif(self._windows[index]['state'] == 2):
                        self._bot.put_heroes_to_work()
                except Exception as e:
                    self._bot_log.error(f"Workflow was broken: {e}")
                    self._bot.refresh()
                    self._utils.await_for_image("./images/connect-wallet-button.png", await_time = self._big_time, tag = "CONNECT")
                    self.try_to_login()
                    self._windows[index]['state'] = 1

    def run(self):
        while True:
            self._put_all_to_work()
            