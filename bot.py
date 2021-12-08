from numpy import true_divide
from pyautogui import *
import pyautogui
import time
import json
import datetime
import random
import logging
from logging.handlers import RotatingFileHandler

class Bot:
    _data = {
        'speed': 1.0,
        'map_time': 2400,
        'map_expected_time_finish': 9000,
        'work_button_confidence': 0.9,
        'default_confidence': 0.9,
        'put_to_work_trys': 45,
        'plataform': 'windows',
        'browser': 'chrome'
    }

    _minimum_time = 0.5
    _small_time = 1
    _medium_time = 5
    _big_time = 20
    _map_time_start = time.perf_counter()

    log_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    my_handler = RotatingFileHandler('./.log', mode='a', maxBytes=1024*1024, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)
    app_log.addHandler(my_handler)

    def __init__(self, config_file = "config.json"):

        config_file = config_file if config_file.find(".json") != -1 else "config.json"
        try:
            with open(config_file, "r") as read_file:
                self._data = json.load(read_file)
        except Exception as e:
            with open(config_file, "w") as write_file:
                json.dump(self._data, write_file, indent=2)

        self._data['speed'] = 1 if self._data['speed'] > 1 else self._data['speed']
        self._minimum_time *= (1/self._data['speed'])
        self._small_time *= (1/self._data['speed'])
        self._medium_time *= (1/self._data['speed'])
        self._big_time *= (1/self._data['speed'])

    def refresh(self):
        self.app_log.info("Refreshing page")
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')
        time.sleep(self.randonTime(self._big_time))
    
    def randonTime(self, time, range = 0.15):
        time += random.randint(-int(time*range), int(time*range))
        return time

    def randon_center(self, box, range = 0.25):
        el_with = box.width
        el_height = box.height
        x, y = pyautogui.center(box)
        x +=  random.randint(-int(el_with*range), int(el_with*range))
        y +=  random.randint(-int(el_height*range), int(el_height*range))
        return x, y

    def randomRangeDecimal(self, value, range):
        return value + random.uniform(-range, range)

    def await_and_click(self, image, await_time, confidance = _data['default_confidence']):
        await_time = int(await_time/2)
        await_time = await_time if await_time > 1 else 2
        self.app_log.info(f"Await and click: {image} for {str(await_time*2)}s")
        for i in range(0, await_time):
            try:
                x, y = self.randon_center(pyautogui.locateOnScreen(image, confidence = confidance))
                time.sleep(self._minimum_time)
                pyautogui.click(x, y)
                self.app_log.info("Image founded and clicked")
                return True
            except:
                time.sleep(2)
        time.sleep(self.randonTime(self._small_time))
        self.app_log.warning("Image not founded")
        return False

    def search_for(self, image, await_time, confidance = _data['default_confidence']):
        await_time = int(await_time)
        self.app_log.info(f"Search for image: {image} for {str(await_time)}s")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                time.sleep(self.randonTime(self._minimum_time))
                self.app_log.info("Image founded")
                return x, y
            except:
                time.sleep(1)
        time.sleep(self.randonTime(self._small_time))
        self.app_log.warning("Image not founded")
        return -1, -1

    def await_for_image(self, image, await_time, confidance = 0.9):
        await_time = int(await_time/2)
        await_time = await_time if await_time > 1 else 2
        self.app_log.info(f"Awaiting {str(await_time*2)}s for {image}")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                i += await_time
                self.app_log.info("Image founded")
                return True
            except:
                time.sleep(2)
        time.sleep(self.randonTime(self._small_time))
        self.app_log.warning("Image not founded")
        return False

    def is_image_present(self, image, confidance = 0.9):
        self.app_log.info(f"Image is present: {image}")
        time.sleep(self.randonTime(self._small_time))
        try:
            founded = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
            self.app_log.info("Image founded")
            return True
        except:
            self.app_log.warning("Image not founded")
            return False

    def try_to_login(self):
        self.app_log.info("Trying to login")
        i = 1
        pyautogui.dragTo(random.randint(90, 130), random.randint(90, 130))
        time.sleep(self.randonTime(self._small_time))
        while(not self.is_image_present("./images/start-pve-button.png")):
            flag = self.await_and_click("./images/connect-wallet-button.png", await_time = self.randonTime(3*self._medium_time))
            if(not flag):
                self.app_log.error("Error while trying to connect")
                self.refresh()
                continue

            self.try_captcha()

            self.app_log.info("Trying to sign metamask")
            if(self._data['plataform'].lower() == 'windows'):
                flag = self.await_and_click("./images/sing-button-windows.png", await_time = self.randonTime(3*self._medium_time))
                if(not flag):
                    self.app_log.error("Error while trying to connect")
                    self.refresh()
                    continue
            else:
                if(self._data['browser'].lower() == 'vivald'):
                    flag = self.await_and_click("./images/sing-button-linux-vivald.png", await_time = self.randonTime(2*self._medium_time))
                else:
                    flag = self.await_and_click("./images/sing-button-linux-chrome.png", await_time = self.randonTime(2*self._medium_time))
                if(not flag):
                    try:
                        x, y = self.search_for("./images/metamask_sign_tab.png", await_time = 2*self._medium_time)
                        if(x == -1):
                            raise ValueError("metamask_sign_tab not founded")
                        pyautogui.click(x, y)
                        time.sleep(self.randonTime(self._small_time))
                        if(self._data['browser'].lower() == 'vivald'):
                            flag = self.await_and_click("./images/sing-button-linux-vivald.png", await_time = self.randonTime(2*self._medium_time))
                        else:
                            flag = self.await_and_click("./images/sing-button-linux-chrome.png", await_time = self.randonTime(2*self._medium_time))
                        time.sleep(self.randonTime(self._small_time))
                        pyautogui.click(x, y)
                        time.sleep(self.randonTime(self._small_time))
                    except Exception as e:
                        self.app_log.error(f"Error while trying to connect: {e}")
                        self.refresh()
                        continue

            flag = self.await_for_image("./images/start-pve-button.png", 3*self._big_time)
            i+=1
            if(not flag):
                self.app_log.error("Error while trying to connect")
                self.refresh()
                continue
        
        self.app_log.info(f"Logged in after {str(i-1)} attempts")

    def click_and_drag(self, box, distance):
        try:
            x, y = self.randon_center(box, range = 0.1)
            pyautogui.moveTo(x, y)
            pyautogui.drag(distance, 0, self.randomRangeDecimal(1.7, 0.2), pyautogui.easeInOutQuad)
        except Exception as e:
            self.app_log.error(f"Error on click_and_drag: {e}")
            raise ValueError("Unable to move")
        
    def find_center_captcha(self, captchaX, captchaY):
        try:
            self.app_log.info("Looking for captcha (1..10s)")
            captchaStart = 72
            captchaX = captchaX + 120
            captchaY = captchaY + 100
            captchaWidth = 160
            captchaHeight = 120
            windowCaptchaRegion=(captchaX, captchaY, captchaWidth, captchaHeight)
            
            ss1 = pyautogui.screenshot(region=windowCaptchaRegion)
            time.sleep(self.randonTime(self._minimum_time))
            ss2 = pyautogui.screenshot(region=windowCaptchaRegion)

            for y in range(0, captchaHeight, 30):
                for x in range(0, captchaWidth, 5):
                    pix = ss1.getpixel((x, y))
                    pix2 = ss2.getpixel((x, y))
                    if (pix != pix2):
                        return captchaStart + x + 22
            self.app_log.info("Captcha not found (adjust formula)")
        except Exception as e:
            self.app_log.error(f"Error on find_center_captcha: {e}")
            raise ValueError("Unable to find center captcha")

    def try_captcha(self):
        if (self.is_image_present("./images/captcha_button.png")):
            self.app_log.info("Trying to solve captcha")
            while True:
                try:
                    #* Window
                    window = pyautogui.locateOnScreen("./images/captcha_window_start.png", confidence = 0.92)
                    windowStart = window.left + window.width
                    windowRegion = (windowStart, window.top, 400, window.height)
                    
                    #* Captcha
                    captchaRegionHorizontalSize = 304
                    captchaDistance = self.find_center_captcha(windowStart, window.top)

                    #* Slider
                    captchaButton = pyautogui.locateOnScreen("./images/captcha_button.png", region=windowRegion, confidence = 0.9)
                    buttonX, buttonY = pyautogui.center(captchaButton)
                    sliderMargin = buttonX - windowStart
                    sliderSize = 400 - sliderMargin * 2

                    #* Calculate crolled distance, click and drag
                    sliderFactor = captchaRegionHorizontalSize / sliderSize
                    sliderDistance = int(captchaDistance / sliderFactor)
                    self.click_and_drag(captchaButton, sliderDistance)

                    if (not self.is_image_present("./images/captcha_button.png")):
                        break
                except Exception as e:
                    self.app_log.error(f"Error on try_captcha: {e}")
                    time.sleep(self.randonTime(self._small_time))
            self.app_log.info("Trying to solve captcha END")

    def scroll_down(self):
        try:
            drag_bars = list(pyautogui.locateAllOnScreen("./images/hero-selection-drag-bar.png", confidence = 0.8))
            x, y = self.randon_center(drag_bars[len(drag_bars)-1])
            time.sleep(self.randonTime(self._minimum_time))
            pyautogui.moveTo(x, y)
            time.sleep(self.randonTime(self._minimum_time))
            pyautogui.dragTo(x, y-200, self._minimum_time, button='left')
            return True
        except Exception as e:
            return False

    def put_heroes_to_work(self):
        self.app_log.info("Trying put heroes to work")
        time.sleep(self.randonTime(self._medium_time))

        puted_heroes_to_work = False
        flag = True
        for i in range (0,5):
            if(puted_heroes_to_work):
                continue

            if(self.is_image_present("./images/back-to-menu-button.png") and not self.is_image_present("./images/hero-selection-drag-bar.png")):
                flag = self.await_and_click("./images/back-to-menu-button.png", self.randonTime(self._big_time))
            elif(self.is_image_present("./images/close-button.png")):
                flag = self.await_and_click("./images/close-button.png", self.randonTime(self._big_time))
            if(not flag):
                self.app_log.error("Unable to go back to menu")
                continue

            if(not self.is_image_present("./images/hero-selection-drag-bar.png")):
                flag = self.await_and_click("./images/heroes-menu-button.png", self.randonTime(self._big_time))
            if(not flag):
                self.app_log.error("heroes-menu-button.png not found")
                continue

            self.try_captcha()

            self.await_for_image("./images/hero-selection-drag-bar.png", self._big_time)
            for i in range(0,4):
                flag = self.scroll_down()
                i = i-1 if not flag else i
                time.sleep(self.randonTime(self._small_time))

            work_buttons = list(pyautogui.locateAllOnScreen('./images/work-button.png', confidence = self._data['work_button_confidence']))
            if(len(work_buttons) > 0):
                x, y = self.randon_center(work_buttons[len(work_buttons)-1], range = 0.1)
                for i in range(0, self._data['put_to_work_trys']):
                    pyautogui.click(x, y)
                    time.sleep(self.randonTime(self._small_time))
                    if(not self.is_image_present('./images/work-button.png', confidance=0.5)):
                        self.await_and_click("./images/close-button.png", self.randonTime(self._medium_time))
                        time.sleep(self.randonTime(self._small_time))
                    elif(not self.is_image_present('./images/work-button.png')):
                        break

            flag = self.await_and_click("./images/close-button.png", self.randonTime(2*self._medium_time))
            flag = self.await_and_click("./images/start-pve-button.png", self.randonTime(2*self._medium_time))
            if(not flag):
                self.app_log.error("Unable to go back to menu after putting heroes to work")
                continue

            puted_heroes_to_work = True

        if(not puted_heroes_to_work):
            raise ValueError("Unable to put heroes to work")

    def reset_map(self):
        self.app_log.info("Redistributing heroes")
        self.await_and_click("./images/back-to-menu-button.png", self.randonTime(self._small_time))
        time.sleep(self.randonTime(self._small_time))
        self.await_and_click("./images/start-pve-button.png", self.randonTime(self._small_time))

    def await_for_new_map(self, await_time, map_expected_time_finish):
        self.app_log.info(f"Awaiting {str(int(await_time / 60))}m for new map")

        time_left = await_time
        while time_left > 0:
            time_start = time.perf_counter()

            if(self.await_and_click("./images/new-map-button.png", self.randonTime(self._medium_time/2))):
                self.app_log.info(f"Map time spent {str(int(map_time_spent / 60))}m")
                self._map_time_start = time.perf_counter()
                self.try_captcha()

            if(self.await_for_image("./images/connect-wallet-button.png", self._medium_time/2)):
                raise ValueError("Captcha failed after 3 attempts")

            if(self.await_and_click("./images/ok-button.png", self.randonTime(self._medium_time/2))):
                raise ValueError("Lost connection")

            map_time_spent = time.perf_counter() - self._map_time_start
            time_progress = await_time - time_left
            time_interval_refresh = time_progress % 70

            if(map_time_spent > map_expected_time_finish and time_interval_refresh > 60):
                self.reset_map()

            time_spent = time.perf_counter() - time_start
            time_left -= time_spent

    #* 1 - login
    #* 2 - Put heroes to work
    #* 3 - Await for a new map
    def select_wat_to_do(self, last_action):
        if(last_action == 0 and not self.is_image_present("./images/start-pve-button.png") and not self.is_image_present("./images/back-to-menu-button.png") and not self.is_image_present("./images/close-button.png")):
            return 1
        elif(last_action == 0 or last_action == 1 or last_action == 3):
            return 2
        elif(last_action == 2 and self.is_image_present("./images/back-to-menu-button.png")):
            return 3
        else:
            return 1

    def run(self):
        state = 0

        while 1:
            random.seed(time.time())
            time.sleep(self.randonTime(self._small_time))
            state = self.select_wat_to_do(state)
            try:
                if(state == 1):
                    self.refresh()
                    self.await_for_image("./images/connect-wallet-button.png", self._big_time)
                    self.try_to_login()
                elif(state == 2):
                    self.put_heroes_to_work()
                else:
                    self.await_for_new_map(self._data['map_time'], self._data['map_expected_time_finish'])
            except Exception as e:
                self.app_log.error(f"Error during workflow: {e}")
                self._map_time_start = time.perf_counter()
                self.refresh()
                self.await_for_image("./images/connect-wallet-button.png", self._big_time)
                self.try_to_login()
                state = 1

pyautogui.FAILSAFE = False
bot = Bot()
while 1:
    try:
        bot.run()
    except Exception as e:
        bot = Bot()
        bot.app_log.error(f"Bot breaking error: {e}")
