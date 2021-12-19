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
        'map_time': 2400,
        'map_expected_time_finish': 9000,
        'work_button_confidence': 0.9,
        'default_confidence': 0.9,
        'put_to_work_trys': 45,
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

    bot_log =None

    def __init__(self, config_file = "config.json"):
        config_file = config_file if config_file.find(".json") != -1 else "config.json"
        try:
            with open(config_file, "r") as read_file:
                self._data = json.load(read_file)
        except Exception as e:
            with open(config_file, "w") as write_file:
                json.dump(self._data, write_file, indent=2)
        
        if (self._data['console_log']):
            self.bot_log = logging
            self.bot_log.basicConfig(format ='[%(asctime)s-%(levelname)s] %(message)s', datefmt='%H:%M:%S', level = logging.DEBUG if self._data['log_level'].lower() == "debug" else logging.INFO)
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
        
    #* A partir da posição atual
    def random_move(self, distanceX, distanceY, range = 5, time = 0.5):
        distanceX = self.random_position(distanceX, range)
        distanceY = self.random_position(distanceY, range)
        duration = self.random_range_decimal(time)
        pyautogui.move(distanceX, distanceY, duration, pyautogui.easeInOutQuad)

    #* Para posição na X/Y
    def random_moveTo(self, box, range = 0.25, time = 0.5):
        x, y = self.randon_center(box, range)
        acceleration = self.random_range_decimal(time)
        pyautogui.moveTo(x, y, acceleration, pyautogui.easeInOutQuad)
        self.random_sleep(self._minimum_time)
        return x, y
        
    #* A partir da posição atual
    def random_drag(self, distanceX, distanceY, range = 5, time = 0.5):
        distanceX = self.random_position(distanceX, range)
        distanceY = self.random_position(distanceY, range)
        acceleration = self.random_range_decimal(time)
        pyautogui.drag(distanceX, distanceY, acceleration, pyautogui.easeInOutQuad)

    def click(self, x, y, time = 0.5):
        actualX, actualY = pyautogui.position()
        if (actualX != x or actualY != y):
            acceleration = self.random_range_decimal(time)
            pyautogui.moveTo(x, y, acceleration, pyautogui.easeInOutQuad)
        pyautogui.click(x, y)
        self.random_sleep(self._minimum_time)
        
    def random_sleep(self, value, range = 0.15):
        time.sleep(self.random_time(value, range))

    def random_position(self, position, range = 5):
        position += random.randint(-int(range), int(range))
        return position
    
    def random_time(self, time, range = 0.15):
        time += random.randint(-int(time*range), int(time*range))
        return time

    def random_range_decimal(self, time, range = 0.25):
        time += random.uniform(time*range, time*range)
        return time

    def randon_center(self, box, range = 0.25):
        el_with = box.width
        el_height = box.height
        x, y = pyautogui.center(box)
        x +=  random.randint(-int(el_with*range), int(el_with*range))
        y +=  random.randint(-int(el_height*range), int(el_height*range))
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
        return  time.perf_counter() - time_start

    def await_and_click(self, image, await_time, confidence = _data['default_confidence'], enableLog = True, tag = "Image"):
        if (enableLog):
            self.bot_log.debug(f"Await and click: {image} for {str(await_time)}s")

        time.sleep(self._minimum_time)
        time_start = time.perf_counter()

        while (self.is_time_out(time_start, await_time) == False):
            box = pyautogui.locateOnScreen(image, confidence = confidence)
            if (box != None):
                x, y = self.random_moveTo(box)
                self.click(x, y)
                if (enableLog):
                    self.bot_log.info(f"{tag} founded and clicked")
                return box
            else:
                time.sleep(2)

        if (enableLog):
            self.bot_log.debug(f"{tag} not founded")
 
        return None

    def await_for_image(self, image, await_time, region: Box = None, confidence = _data['default_confidence'], enableLog = True, tag = "Image"):
        if (enableLog):
            self.bot_log.debug(f"Awaiting {str(await_time)}s for {image}")
        time.sleep(self._minimum_time)
        time_start = time.perf_counter()

        while (self.is_time_out(time_start, await_time) == False):
            box = pyautogui.locateOnScreen(image, region=region, confidence = confidence)
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

    def is_image_present(self, image, confidence = _data['default_confidence'], enableLog = True, tag = "Image"):
        if (enableLog):
            self.bot_log.debug(f"Checking if image is present: {image}")
        time.sleep(self._minimum_time)
        if (pyautogui.locateOnScreen(image, confidence = confidence) != None):
            if (enableLog):
                self.bot_log.info(f"{tag} founded")
            return True
        else:
            if (enableLog):
                self.bot_log.debug(f"{tag} not founded")
            return False

    def try_to_login(self):
        self.random_move(-300, -100)
        maxAttempts = 10
        for attempt in range(maxAttempts):
            self.bot_log.info(f"{attempt + 1}/{maxAttempts} Trying to login")

            if (self.await_and_click("./images/connect-wallet-button.png", await_time = 2*self._medium_time, tag = "CONNECT") == None):
                self.bot_log.error("Error while trying to connect")
                self.random_move(-300, -100)
                self.refresh()
                continue

            if (not self.try_captcha()):
                continue
            
            if (self.await_and_click("./images/ok-button.png", await_time = self._small_time, tag = "OK")):
                self.bot_log.error("Lost connection")
                time.sleep(2*self._medium_time)
                continue

            self.bot_log.info("Trying to sign metamask")
            if (self._data['plataform'].lower() == 'windows'):
                if (self.await_and_click("./images/sing-button-windows.png", await_time = self._big_time, tag = "SIGN") == None):
                    self.bot_log.error("METAMASK_SIGN not founded")
                    self.move_and_refresh(-300, -100)
                    continue
            else:
                if(self._data['browser'].lower() == 'vivald'):
                    box = self.await_and_click("./images/sing-button-linux-vivald.png", await_time = self._big_time, tag = "SIGN")
                else:
                    box = self.await_and_click("./images/sing-button-linux-chrome.png", await_time = self._big_time, tag = "SIGN")

                if (box == None):
                    if (self._data['browser'].lower() == 'vivald'):
                        box = self.await_and_click("./images/metamask_sign_tab_vivald.png", await_time = self._big_time, tag = "METAMASK")
                    else:
                        box = self.await_and_click("./images/metamask_sign_tab_chrome.png", await_time = self._big_time, tag = "METAMASK")

                    if (box == None):
                        self.bot_log.error("METAMASK_TAB not founded")
                        self.move_and_refresh(-300, -100)
                        continue

                    if (self._data['browser'].lower() == 'vivald'):
                        box = self.await_and_click("./images/sing-button-linux-vivald.png", await_time = self._big_time, tag = "SIGN")
                    else:
                        box = self.await_and_click("./images/sing-button-linux-chrome.png", await_time = self._big_time, tag = "SIGN")

                if (box == None):
                    self.bot_log.error("METAMASK_SIGN not founded")
                    self.move_and_refresh(-400, 100)
                    continue

            self.bot_log.info("Waiting to start")
            maxAttemptsAwait = 20
            for i in range(maxAttemptsAwait):

                if (self.await_for_image("./images/start-pve-button.png", await_time = self._medium_time, tag = "PVE")):
                    self.bot_log.info(f"Logged in after {attempt + 1} attempts")
                    return

                if (self.await_and_click("./images/ok-button.png", await_time = self._small_time, tag = "OK")):
                    self.random_move(-300, -100)
                    time.sleep(2*self._medium_time)
                    if (attempt + 1 == maxAttempts):
                        raise ValueError(f"Failed after {maxAttempts} attempts")
                    break

                if (i + 1 == maxAttemptsAwait):                    
                    self.bot_log.info("Time to start is over")
                    self.move_and_refresh(-300, -100)

        raise ValueError(f"Failed after {maxAttempts} attempts")
        
    def try_captcha(self):
        window = self.await_for_image("./images/captcha_window.png", await_time = self._minimum_time, confidence = 0.92, tag = "CAPTCHA")
        if (window != None):
            self.bot_log.info("Awaiting YOU solve the captcha")

            while (self.is_image_present("./images/captcha_window.png", confidence = 0.92, enableLog = False, tag = "CAPTCHA")):
                time.sleep(self._medium_time)
                
                if (self.await_and_click("./images/ok-button.png", await_time = self._small_time, tag = "OK")):
                    self.bot_log.error("Lost connection")
                    time.sleep(2*self._medium_time)
                    return False
            
            return True

            self.bot_log.info("Captcha START")
            try:
                while True:
                    #* Window
                    windowCaptchaOneRegion = Box(window.left + 85, window.top + 150, 185, 70)
                    windowCaptchaTwoRegion = Box(window.left + 75, window.top + 120, 420, 140)
                    windowSliderRegion = Box(window.left, window.top + 350, 520, 80)

                    #* Slider
                    captchaButton = self.await_for_image("./images/captcha_button.png", await_time = self._small_time, region = windowSliderRegion, tag = "SLIDER")
                    buttonX, buttonY = pyautogui.center(captchaButton)
                    sliderMargin = buttonX - window.left
                    sliderSize = 520 - sliderMargin * 2

                    #* Captcha locate
                    first, second, third = self.find_captcha(windowCaptchaOneRegion)
                    self.bot_log.info(f"Trying find captcha: {first}{second}{third}")

                    #* Calculate scrolled distance, click and move
                    self.random_moveTo(captchaButton, range = 0.1)
                    sliderDistance = int(sliderSize / 4)

                    pyautogui.mouseDown()
                    for i in range(5):
                        if (i == 1):
                            self.random_move(-sliderDistance, 0, time = 0.6)
                        elif (i == 2):
                            self.random_move(sliderDistance * 2, 0, time = 0.6)
                        else:
                            self.random_move(sliderDistance, 0, time = 0.6)
                        if (self.find_captcha_two(windowCaptchaTwoRegion, first, second, third, i)):
                            break
                    pyautogui.mouseUp()

                    if (not self.is_image_present("./images/captcha_button.png", enableLog = False, tag = "SLIDER")):
                        self.bot_log.info("Captcha END")
                        break
            except Exception as e:
                self.bot_log.error(f"Error on try_captcha: {e}")
                raise ValueError("Unable to Try Captcha")

        return True

    def find_captcha(self, box: Box):
        self.bot_log.info("Trying find captcha")
        try:
            numbers = []
            count = 0
            for i in range(10):
                number = pyautogui.locateOnScreen(f"./images/{i}.png", region=box, confidence = 0.92)
                if (number != None): 
                    numbers.append((i, number.left))
                    count += 1
                    if (count == 3):
                        break
            numbersOrderned = sorted(numbers, key=lambda elem: elem[1])
            return [elem[0] for elem in numbersOrderned]
        except Exception as e:
            self.bot_log.error(f"Error on find_captcha: {e}")
            raise ValueError("Unable to Find Captcha")

    def find_captcha_two(self, box: Box, first, second, third, whileIndex):
        try:
            ss = pyautogui.screenshot(region = box)

            white = (255, 255, 255)
            brown = (186, 113, 86)
            numbersToFind = (first, second, third)
            numbers = (
                [0, 106, ([10, 0, white], [35, -90, white], [55, 0, white]), 71], #100%
                [1, 120, ([3, -110, white], [6, -110, white], [13, 8, white]), 20], #100%
                [2, 110, ([33, -100, white], [40, 10, white], [80, 18, white]), 85], #100%
                [3, 17, ([40, 13, white], [57, 79, white], [54, 87, white]), 70], #50%
                [4, 28, ([7, 0, white], [40, 90, white], [50, 0, white]), 60], #90#
                [5, 114, ([10, -9, white], [14, -82, white], [65, -19, white]), 73], #75%
                [6, 100, ([15, -72, white], [38, 0, white], [65, -5, white]), 76], #100%
                [7, 113, ([10, 5, white], [16, -18, white], [28, -85, white]), 20], #75%
                [8, 99, ([3, -4, white], [4, -4, white], [57, -66, white]), 72], #50%
                [9, 106, ([-5, -73, white], [10, -11, white], [11, 4, white]), 19] #50
            )

            marginX = 0
            marginY = 0
            pixelWhiteSize = 0
            numberMinSize = 11
            numberPosition = 0
            numberToFind = numbersToFind[numberPosition]
            while (marginX < box.width):
                try:
                    marginY = numbers[numberToFind][1]
                    pixels = numbers[numberToFind][2]
                    nextNumberStart = numbers[numberToFind][3]
                    if (ss.getpixel((marginX, marginY)) == white):

                        pixelWhiteSize += 1
                        if (pixelWhiteSize == numberMinSize):
                            marginX -= numberMinSize - 1
                            pixelWhiteSize = 0
                            if (self._data['log_level'].lower() == "debug"):
                                ss.putpixel((marginX, marginY), (0, 128, 0))

                            localizedAllPixels = 0
                            for pixel in pixels:
                                pixX = pixel[0]
                                pixY = pixel[1]
                                color = pixel[2]
                                if (ss.getpixel((marginX + pixX, marginY + pixY)) == color): 
                                    localizedAllPixels += 1
                                if (self._data['log_level'].lower() == "debug"):
                                    ss.putpixel((marginX + pixX, marginY + pixY), (255, 0, 0))

                            if (localizedAllPixels == 3):
                                marginX = marginX + nextNumberStart
                            else:
                                self.bot_log.info(f"#{whileIndex + 1} not find: {numberToFind}")
                                if (self._data['log_level'].lower() == "debug"):
                                    ss.save(f'my_screenshot_{whileIndex + 1}.png')
                                return False

                            numberPosition += 1
                            if (numberPosition < 3):
                                numberToFind = numbersToFind[numberPosition]
                            else:
                                self.bot_log.info(f"#{whileIndex + 1} find all")
                    else:
                        pixelWhiteSize = 0

                    marginX += 1
                except Exception as e:
                    print(e)
                    return False
            if (self._data['log_level'].lower() == "debug"):
                ss.save(f'my_screenshot_{whileIndex + 1}.png')
            return True
        except Exception as e:
            self.bot_log.error(f"Error on find_captcha_two: {e}")
            raise ValueError("Unable to Find Captcha Two")

    def scroll_down(self):
        try:
            drag_bars = list(pyautogui.locateAllOnScreen("./images/hero-selection-drag-bar.png", confidence = 0.8))
            drag = drag_bars[len(drag_bars)-1]
            self.random_moveTo(drag)
            self.random_drag(0, -200, time = 0.4)
            self.random_sleep(self._minimum_time)
            return True
        except Exception as e:
            self.bot_log.error(f"Error on scroll_down: {e}")
            return False

    def put_heroes_to_work(self):
        self.bot_log.info("Trying put heroes to work")
        self.random_sleep(self._medium_time)

        puted_heroes_to_work = False
        stopFlow = False

        for i in range (5):
            #* PVE screen
            if (self.is_image_present("./images/back-to-menu-button.png", tag = "BACK") and not self.is_image_present("./images/hero-selection-drag-bar.png", tag = "HERO")):
                stopFlow = self.await_and_click("./images/back-to-menu-button.png", await_time = self._big_time, tag = "BACK") == None
            #* Main screen
            elif (self.is_image_present("./images/close-button.png", tag = "CLOSE")):
                stopFlow = self.await_and_click("./images/close-button.png", await_time = self._big_time, tag = "CLOSE") == None

            if (stopFlow):
                self.bot_log.error("Unable to go back to menu")
                continue

            #* Heroes screen
            if (not self.is_image_present("./images/hero-selection-drag-bar.png", tag = "HERO")):
                stopFlow = self.await_and_click("./images/heroes-menu-button.png", await_time = self._big_time, tag = "HEROES") == None
            if (stopFlow):
                self.bot_log.error("heroes-menu-button.png not found")
                continue

            if (not self.try_captcha()):
                return
            
            self.bot_log.info("Waiting for heroes")
            maxAttemptsAwait = 12
            for attempt in range(maxAttemptsAwait):

                if (self.await_for_image("./images/hero-selection-drag-bar.png", await_time = self._medium_time, enableLog = False, tag = "HERO") == None):
                    if (self.await_and_click("./images/ok-button.png", await_time = self._small_time, tag = "OK")):
                        self.bot_log.error("Lost connection")
                        return

                    if (self.is_image_present("./images/connect-wallet-button.png", tag = "CONNECT")):
                        self.bot_log.error("Failed after 3 attempts")
                        return
                else:
                    break

                if (attempt + 1 == maxAttemptsAwait):
                    self.bot_log.error("Time for heroes is over")       
                    self.move_and_refresh(-300, -100)      
                    return
                    
            self.bot_log.info("Searching for work buttons")
            for i in range(3):
                flag = self.scroll_down()
                i = i-1 if not flag else i
            
            work_buttons = list(pyautogui.locateAllOnScreen('./images/work-button.png', confidence = self._data['work_button_confidence']))
            self.bot_log.info(f"{len(work_buttons)} work buttons founded")
            
            self.bot_log.info("Putting heroes to work")
            if (len(work_buttons) > 0):
                box = work_buttons[len(work_buttons)-1]
                x, y = self.random_moveTo(box)

                for i in range(0, self._data['put_to_work_trys']):
                    self.click(x, y)
                    if (not self.is_image_present('./images/work-button.png', confidence = 0.5, enableLog = False, tag = "WORK")):
                        self.await_and_click("./images/close-button.png", await_time = self._medium_time, tag = "CLOSE")
                    elif (not self.is_image_present('./images/work-button.png', confidence = self._data['work_button_confidence'], enableLog = False, tag = "WORK")):
                        break

            stopFlow = self.await_and_click("./images/close-button.png", await_time = 2*self._medium_time, tag = "CLOSE") == None
            stopFlow = self.await_and_click("./images/start-pve-button.png", await_time = 2*self._medium_time, tag = "PVE") == None

            if (stopFlow):
                self.bot_log.error("Unable to go back to menu after putting heroes to work")
                continue

            self.bot_log.info("Done putting heroes to work")
            puted_heroes_to_work = True
            break

        if (not puted_heroes_to_work):
            raise ValueError("Unable to put heroes to work")

    def reset_map(self):
        self.bot_log.info("Redistributing heroes")
        self.await_and_click("./images/back-to-menu-button.png", await_time = self._small_time, enableLog = False, tag = "BACK")
        self.await_and_click("./images/start-pve-button.png", await_time = self._small_time, enableLog = False, tag = "PVE")

    def await_for_new_map(self, await_time, map_expected_time_finish):
        self.bot_log.info(f"Awaiting {str(int(await_time / 60))}m for new map")
        time_start = time.perf_counter()

        while (self.is_time_out(time_start, await_time) == False):
            map_time_spent = self.time_spent(self._map_time_start)

            if (self.await_and_click("./images/new-map-button.png", await_time = self._medium_time, tag = "NEW") != None):
                self.bot_log.info(f"Map time spent {str(int(map_time_spent / 60))}m")
                self._map_time_start = time.perf_counter()

                if (not self.try_captcha()):
                    return

                if (self.await_and_click("./images/ok-button.png", await_time = self._small_time, tag = "OK")):
                    self.bot_log.error("Lost connection")
                    return

                if (self.await_and_click("./images/connect-wallet-button.png", await_time = self._medium_time, tag = "CONNECT") != None):
                    self.bot_log.error("Failed after 3 attempts")
                    return

            time_interval_refresh = self.time_spent(time_start) % 70

            if(map_time_spent > map_expected_time_finish and time_interval_refresh > 60):
                if (not self.is_image_present('./images/ok-button.png', enableLog = False, tag = "OK")):
                    self.reset_map()
        
        if (self.await_and_click("./images/ok-button.png", await_time = self._small_time, tag = "OK")):
            raise ValueError("Lost connection")

    #* 1 - login
    #* 2 - Put heroes to work
    #* 3 - Await for a new map
    def select_wat_to_do(self, last_action):
        if(last_action == 0 and not self.is_image_present("./images/start-pve-button.png", tag = "PVE") and not self.is_image_present("./images/back-to-menu-button.png", tag = "BACK") and not self.is_image_present("./images/close-button.png", tag = "CLOSE")):
            return 1
        elif(last_action == 0 or last_action == 1 or last_action == 3):
            return 2
        elif(last_action == 2 and self.is_image_present("./images/back-to-menu-button.png", tag = "BACK")):
            return 3
        else:
            return 1

    def run(self):
        state = 0

        while True:
            random.seed(time.time())
            time.sleep(2*self._medium_time)
            state = self.select_wat_to_do(state)
            try:
                if(state == 1):
                    self.await_for_image("./images/connect-wallet-button.png", await_time = self._big_time, tag = "CONNECT")
                    self.try_to_login()
                elif(state == 2):
                    self.put_heroes_to_work()
                else:
                    self.await_for_new_map(self.random_time(self._data['map_time']), self._data['map_expected_time_finish'])
            except Exception as e:
                self.bot_log.error(f"Workflow was broken: {e}")
                self.refresh()
                self.await_for_image("./images/connect-wallet-button.png", await_time = self._big_time, tag = "CONNECT")
                self.try_to_login()
                state = 1

pyautogui.FAILSAFE = False
bot = Bot()
while True:
    try:
        bot.run()
    except Exception as e:
        bot = Bot()
        # bot.bot_log.error(f"Bot breaking error: {e}")
