from numpy import true_divide
from pyautogui import *
import pyautogui
import time
import json
import random
import logging
from logging.handlers import RotatingFileHandler
from pyscreeze import Box


class Bot:
    _data = {
        'speed': 1.0,
        'map_time': 3000,
        'work_button_confidence': 0.9,
        'default_confidence': 0.9,
        'plataform': 'windows',
        'browser': 'chrome',
        "console_log": True,
        "log_level": "info"
    }

    _minimum_time = 0.5
    _small_time = 1
    _medium_time = 5
    _big_time = 20
    _map_time_start = time.perf_counter()

    bot_log = None

    def __init__(self, config_file="config.json"):
        config_file = config_file if config_file.find(".json") != -1 else "config.json"
        try:
            with open(config_file, "r") as read_file:
                self._data = json.load(read_file)
        except Exception as e:
            with open(config_file, "w") as write_file:
                json.dump(self._data, write_file, indent=2)

        if (self._data['console_log']):
            self.bot_log = logging
            self.bot_log.basicConfig(
                format='[%(asctime)s-%(levelname)s] %(message)s', 
                datefmt='%H:%M:%S', 
                level=logging.DEBUG if self._data['log_level'].lower() == "debug" else logging.INFO
            )
        else:
            log_formatter = logging.Formatter('[%(asctime)s-%(levelname)s] %(message)s', datefmt='%H:%M:%S')
            my_handler = RotatingFileHandler('./.log', mode='a', maxBytes=1024*1024, encoding=None, delay=0)
            my_handler.setFormatter(log_formatter)
            my_handler.setLevel(logging.DEBUG if self._data['log_level'].lower() == "debug" else logging.INFO)
            self.bot_log = logging.getLogger('root')
            self.bot_log.setLevel(logging.DEBUG if self._data['log_level'].lower() == "debug" else logging.INFO)
            self.bot_log.addHandler(my_handler)

        self._data['speed'] = 1 if self._data['speed'] > 1 else self._data['speed']
        self._minimum_time *= (1/self._data['speed'])
        self._small_time *= (1/self._data['speed'])
        self._medium_time *= (1/self._data['speed'])
        self._big_time *= (1/self._data['speed'])

    def refresh(self):
        self.bot_log.info("Refreshing page")
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')
        self.random_sleep(self._big_time)

    # * A partir da posição atual
    def random_move(self, distanceX, distanceY, range=5, time=0.5):
        distanceX = self.random_position(distanceX, range)
        distanceY = self.random_position(distanceY, range)
        duration = self.random_range_decimal(time)
        pyautogui.move(distanceX, distanceY, duration, pyautogui.easeInOutQuad)

    # * Para posição na X/Y
    def random_moveTo(self, box, range=0.25, time=0.5):
        x, y = self.randon_center(box, range)
        acceleration = self.random_range_decimal(time)
        pyautogui.moveTo(x, y, acceleration, pyautogui.easeInOutQuad)
        self.random_sleep(self._minimum_time)
        return x, y

    # * A partir da posição atual
    def random_drag(self, distanceX, distanceY, range=5, time=0.5):
        distanceX = self.random_position(distanceX, range)
        distanceY = self.random_position(distanceY, range)
        acceleration = self.random_range_decimal(time)
        pyautogui.drag(distanceX, distanceY, acceleration, pyautogui.easeInOutQuad)

    def click(self, x, y, time=0.5):
        actualX, actualY = pyautogui.position()
        if (actualX != x or actualY != y):
            acceleration = self.random_range_decimal(time)
            pyautogui.moveTo(x, y, acceleration, pyautogui.easeInOutQuad)
        pyautogui.click(x, y)
        self.random_sleep(self._minimum_time)

    def random_sleep(self, value, range=0.15):
        time.sleep(self.random_time(value, range))

    def random_position(self, position, range=5):
        position += random.randint(-int(range), int(range))
        return position

    def random_time(self, time, range=0.15):
        time += random.randint(-int(time*range), int(time*range))
        return time

    def random_range_decimal(self, time, range=0.25):
        time += random.uniform(time*range, time*range)
        return time

    def randon_center(self, box, range=0.25):
        el_with = box.width
        el_height = box.height
        x, y = pyautogui.center(box)
        x += random.randint(-int(el_with*range), int(el_with*range))
        y += random.randint(-int(el_height*range), int(el_height*range))
        return x, y

    def move_and_refresh(self, x, y):
        self.random_move(x, y)
        x, y = pyautogui.position()
        self.click(x, y)
        self.refresh()

    def is_time_out(self, time_start, await_time):
        time_spent = time.perf_counter() - time_start
        return True if time_spent >= await_time else False

    def time_spent(self, time_start):
        return time.perf_counter() - time_start

    def await_and_click(self, image, await_time, confidence=_data['default_confidence'], enableLog=True, tag="Image"):
        if (enableLog):
            self.bot_log.debug(f"Await and click: {image} for {str(await_time)}s")

        time.sleep(self._minimum_time)
        time_start = time.perf_counter()

        while (self.is_time_out(time_start, await_time) == False):
            box = pyautogui.locateOnScreen(image, confidence=confidence)
            if (box != None):
                x, y = self.random_moveTo(box)
                self.click(x, y)
                if (enableLog):
                    self.bot_log.info(f"{tag} clicked")
                return box
            else:
                time.sleep(2)

        if (enableLog):
            self.bot_log.debug(f"{tag} not founded")

        return None

    def await_for_image(self, image, await_time, region: Box = None, confidence=_data['default_confidence'], enableLog=True, tag="Image"):
        if (enableLog):
            self.bot_log.debug(f"Awaiting {str(await_time)}s for {image}")
        time.sleep(self._minimum_time)
        time_start = time.perf_counter()

        while (self.is_time_out(time_start, await_time) == False):
            box = pyautogui.locateOnScreen(image, region=region, confidence=confidence)
            if (box != None):
                if (enableLog):
                    self.bot_log.info(f"{tag} founded")
                return box
            else:
                time.sleep(2)

        self.random_sleep(self._small_time)
        if (enableLog):
            self.bot_log.debug(f"{tag} not founded")
        return None

    def is_image_present(self, image, confidence=_data['default_confidence'], enableLog=True, tag="Image"):
        if (enableLog):
            self.bot_log.debug(f"Checking if image is present: {image}")
        time.sleep(self._minimum_time)
        if (pyautogui.locateOnScreen(image, confidence=confidence) != None):
            if (enableLog):
                self.bot_log.info(f"{tag} founded")
            return True
        else:
            if (enableLog):
                self.bot_log.debug(f"{tag} not founded")
            return False

    def try_to_login(self):
        maxAttempts = 10
        for attempt in range(maxAttempts):
            self.bot_log.info(f"{attempt + 1}/{maxAttempts} Trying to login")

            if (self.await_and_click("./images/connect-wallet-button.png", await_time=2*self._medium_time, tag="CONNECT") == None):
                self.bot_log.error("Error while trying to connect")
                self.random_move(-300, -100)
                self.refresh()
                continue

            if (self.await_and_click("./images/ok-button.png", await_time=self._small_time, tag="OK")):
                self.bot_log.error("Lost connection")
                time.sleep(2*self._medium_time)
                continue

            self.bot_log.info("Trying to sign metamask")
            if (self._data['plataform'].lower() == 'windows'):
                if (self.await_and_click("./images/sing-button-windows.png", await_time=self._big_time, tag="SIGN") == None):
                    self.bot_log.error("METAMASK_SIGN not founded")
                    self.move_and_refresh(-300, -100)
                    continue
            else:
                if(self._data['browser'].lower() == 'vivald'):
                    box = self.await_and_click("./images/sing-button-linux-vivald.png", await_time=self._big_time, tag="SIGN")
                else:
                    box = self.await_and_click("./images/sing-button-linux-chrome.png", await_time=self._big_time, tag="SIGN")

                if (box == None):
                    if (self._data['browser'].lower() == 'vivald'):
                        box = self.await_and_click("./images/metamask_sign_tab_vivald.png", await_time=self._big_time, tag="METAMASK")
                    else:
                        box = self.await_and_click("./images/metamask_sign_tab_chrome.png", await_time=self._big_time, tag="METAMASK")

                    if (box == None):
                        self.bot_log.error("METAMASK_TAB not founded")
                        self.move_and_refresh(-300, -100)
                        continue

                    if (self._data['browser'].lower() == 'vivald'):
                        box = self.await_and_click("./images/sing-button-linux-vivald.png", await_time=self._big_time, tag="SIGN")
                    else:
                        box = self.await_and_click("./images/sing-button-linux-chrome.png", await_time=self._big_time, tag="SIGN")

                if (box == None):
                    self.bot_log.error("METAMASK_SIGN not founded")
                    self.move_and_refresh(-400, 100)
                    continue

            self.bot_log.info("Waiting to start")
            maxAttemptsAwait = 20
            for i in range(maxAttemptsAwait):

                if (self.await_for_image("./images/start-pve-button.png", await_time=self._medium_time, tag="PVE")):
                    self.bot_log.info(f"Logged in after {attempt + 1} attempts")
                    return

                if (self.await_and_click("./images/ok-button.png", await_time=self._small_time, tag="OK")):
                    self.random_move(-300, -100)
                    time.sleep(2*self._medium_time)
                    if (attempt + 1 == maxAttempts):
                        raise ValueError(f"Failed after {maxAttempts} attempts")
                    break

                if (i + 1 == maxAttemptsAwait):
                    self.bot_log.info("Time to start is over")
                    self.move_and_refresh(-300, -100)

        raise ValueError(f"Failed after {maxAttempts} attempts")

    def put_heroes_to_work(self):
        self.bot_log.info("Trying put heroes to work")
        self.random_sleep(self._small_time)

        puted_heroes_to_work = False
        stopFlow = False

        for i in range(5):
            # * PVE screen
            if (self.is_image_present("./images/back-to-menu-button.png", enableLog=False, tag="BACK")):
                stopFlow = self.await_and_click("./images/back-to-menu-button.png", await_time=self._big_time, tag="BACK") == None
            # * Main screen
            elif (self.is_image_present("./images/close-button.png", enableLog=False, tag="CLOSE")):
                stopFlow = self.await_and_click("./images/close-button.png", await_time=self._big_time, tag="CLOSE") == None

            if (stopFlow):
                self.bot_log.error("Unable to go back to menu")
                continue

            # * Heroes screen
            if (not self.is_image_present("./images/heroes-work-all-button.png", confidence=self._data['work_button_confidence'], tag="WORK")):
                stopFlow = self.await_and_click("./images/heroes-menu-button.png", await_time=self._big_time, tag="HEROES") == None
            if (stopFlow):
                self.bot_log.error("heroes-menu-button.png not found")
                continue

            self.bot_log.info("Trying to put all heroes to work")
            maxAttemptsAwait = 10
            for attempt in range(maxAttemptsAwait):
                self.await_and_click("./images/heroes-work-all-button.png", await_time=self._small_time, confidence=self._data['work_button_confidence'], tag="WORK")

                if (self.is_image_present('./images/heroes-work-all-finish.png', confidence=self._data['work_button_confidence'], enableLog=False, tag="WORK")):
                    break
                
                if (self.await_and_click("./images/ok-button.png", await_time=self._small_time, tag="OK")):
                    self.bot_log.error("Lost connection")
                    return
                
                if (attempt + 1 == maxAttemptsAwait):
                    self.bot_log.error("Time for heroes is over")
                    self.move_and_refresh(-300, -100)
                    return
                
                time.sleep(self._medium_time)

            stopFlow = self.await_and_click("./images/close-button.png", await_time=2*self._medium_time, tag="CLOSE") == None
            stopFlow = self.await_and_click("./images/start-pve-button.png", await_time=2*self._medium_time, tag="PVE") == None

            if (stopFlow):
                self.bot_log.error("Unable to go back to menu after putting heroes to work")
                continue

            self.bot_log.info("Done putting heroes to work")
            puted_heroes_to_work = True
            break

        if (not puted_heroes_to_work):
            raise ValueError("Unable to put heroes to work")

    def await_for_new_map(self, await_time):
        self.bot_log.info(f"Awaiting {str(int(await_time / 60))}m for new map")

        map_time_start = time.perf_counter()
        is_map_time_finish = False

        self.check_connection()

        while (is_map_time_finish == False):
            map_time_spent = self.time_spent(self._map_time_start)
            is_map_time_finish = self.is_time_out(map_time_start, await_time)

            if (self.await_and_click("./images/new-map-button.png", await_time=self._medium_time, tag="NEW") != None):
                self.bot_log.info(f"Map time spent {str(int(map_time_spent / 60))}m")
                self._map_time_start = time.perf_counter()

                if (self.await_and_click("./images/ok-button.png", await_time=self._big_time, tag="OK")):
                    raise ValueError("Lost connection")

            if (self.time_spent(map_time_start) % 260 > 250):
                self.check_connection()
            
            if (self.time_spent(map_time_start) < 300 or is_map_time_finish):
                if (self.await_and_click("./images/ok-button.png", await_time=self._small_time, tag="OK")):
                    raise ValueError("Lost connection")

    def check_connection(self):
        if (not self.is_image_present('./images/ok-button.png', enableLog=False, tag="OK")):
            self.bot_log.info("Checking connection")
            self.await_and_click("./images/chest-button.png", await_time=self._small_time, enableLog=False, tag="CHEST")
            self.await_and_click("./images/close-button.png", await_time=self._small_time, enableLog=False, tag="CLOSE")

    # * 1 - login
    # * 2 - Put heroes to work
    # * 3 - Await for a new map
    def select_wat_to_do(self, last_action):
        if(last_action == 0 and not self.is_image_present("./images/start-pve-button.png", tag="PVE") and not self.is_image_present("./images/back-to-menu-button.png", tag="BACK") and not self.is_image_present("./images/close-button.png", tag="CLOSE")):
            return 1
        elif(last_action == 0 or last_action == 1 or last_action == 3):
            return 2
        elif(last_action == 2 and self.is_image_present("./images/back-to-menu-button.png", tag="BACK")):
            return 3
        else:
            return 1

    def run(self):
        state = 0

        while True:
            random.seed(time.time())
            time.sleep(2*self._small_time)
            state = self.select_wat_to_do(state)
            try:
                if(state == 1):
                    self.await_for_image("./images/connect-wallet-button.png", await_time=self._big_time, tag="CONNECT")
                    self.try_to_login()
                elif(state == 2):
                    self.put_heroes_to_work()
                else:
                    self.await_for_new_map(self.random_time(self._data['map_time']))
            except Exception as e:
                self.bot_log.error(f"Workflow was broken: {e}")
                self.refresh()
                state = 0

pyautogui.FAILSAFE = False
bot = Bot()
while True:
    try:
        bot.run()
    except Exception as e:
        bot = Bot()
