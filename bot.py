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
        'work_button_confidence': 0.92,
        'default_confidence': 0.92,
        'put_to_work_trys': 45,
        'plataform': 'windows',
        'browser': 'chrome'
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

        if(self._data['console_log']):
            self.bot_log = logging
            self.bot_log.basicConfig(format ='[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
        else:
            log_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S')
            my_handler = RotatingFileHandler('./.log', mode='a', maxBytes=1024*1024, encoding=None, delay=0)
            my_handler.setFormatter(log_formatter)
            my_handler.setLevel(logging.INFO)
            self.bot_log = logging.getLogger('root')
            self.bot_log.setLevel(logging.INFO)
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
        time.sleep(self.randonTime(self._big_time))
    
    def randonMove(self, position, range = 2):
        position += random.randint(-int(position+range), int(position+range))
        return position
    
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
        # self.bot_log.info(f"Await and click: {image} for {str(await_time*2)}s")
        for i in range(0, await_time):
            try:
                x, y = self.randon_center(pyautogui.locateOnScreen(image, confidence = confidance))
                pyautogui.moveTo(x, y)
                time.sleep(self.randonTime(self._minimum_time))
                pyautogui.click(x, y)
                self.bot_log.info("Image founded and clicked")
                return True
            except:
                time.sleep(2)
        time.sleep(self.randonTime(self._small_time))
        # self.bot_log.warning("Image not founded")
        return False

    def search_for(self, image, await_time, confidance = _data['default_confidence']):
        await_time = int(await_time)
        # self.bot_log.info(f"Search for image: {image} for {str(await_time)}s")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                time.sleep(self.randonTime(self._minimum_time))
                # self.bot_log.info("Image founded")
                return x, y
            except:
                time.sleep(1)
        time.sleep(self.randonTime(self._small_time))
        # self.bot_log.warning("Image not founded")
        return -1, -1

    def await_for_image(self, image, await_time, confidance = 0.9):
        await_time = int(await_time/2)
        await_time = await_time if await_time > 1 else 2
        # self.bot_log.info(f"Awaiting {str(await_time*2)}s for {image}")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                i += await_time
                # self.bot_log.info("Image founded")
                return True
            except:
                time.sleep(2)
        time.sleep(self.randonTime(self._small_time))
        # self.bot_log.warning("Image not founded")
        return False

    def is_image_present(self, image, confidance = 0.9):
        # self.bot_log.info(f"Image is present: {image}")
        time.sleep(self.randonTime(self._small_time))
        try:
            founded = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
            # self.bot_log.info("Image founded")
            return True
        except:
            # self.bot_log.warning("Image not founded")
            return False

    def try_to_login(self):
        self.bot_log.info("Trying to login")
        i = 1
        pyautogui.dragTo(random.randint(90, 130), random.randint(90, 130))
        time.sleep(self.randonTime(self._small_time))
        while(not self.is_image_present("./images/start-pve-button.png")):
            flag = self.await_and_click("./images/connect-wallet-button.png", await_time = self.randonTime(3*self._medium_time))
            if(not flag):
                self.bot_log.error("Error while trying to connect")
                self.refresh()
                continue

            self.try_captcha()

            self.bot_log.info("Trying to sign metamask")
            if(self._data['plataform'].lower() == 'windows'):
                flag = self.await_and_click("./images/sing-button-windows.png", await_time = self.randonTime(3*self._medium_time))
                if(not flag):
                    self.bot_log.error("Error while trying to connect")
                    self.refresh()
                    continue
            else:
                if(self._data['browser'].lower() == 'vivald'):
                    flag = self.await_and_click("./images/sing-button-linux-vivald.png", await_time = self.randonTime(2*self._medium_time))
                else:
                    flag = self.await_and_click("./images/sing-button-linux-chrome.png", await_time = self.randonTime(2*self._medium_time))
                if(not flag):
                    try:
                        if(self._data['browser'].lower() == 'vivald'):
                            x, y = self.search_for("./images/metamask_sign_tab_vivald.png", await_time = self.randonTime(2*self._medium_time))
                        else:
                            x, y = self.search_for("./images/metamask_sign_tab_chrome.png", await_time = self.randonTime(*self._medium_time))
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
                        self.bot_log.error(f"Error while trying to connect: {e}")
                        self.refresh()
                        continue

            flag = self.await_for_image("./images/start-pve-button.png", 3*self._big_time)
            i+=1
            if(not flag):
                self.bot_log.error("Error while trying to connect")
                self.refresh()
                continue
        
        self.bot_log.info(f"Logged in after {str(i-1)} attempts")
        
    def try_captcha(self):
        self.bot_log.info("Captcha flow start")
        time.sleep(self._minimum_time)

        window = pyautogui.locateOnScreen("./images/captcha_window.png", confidence = 0.92)
        if (window != None):
            while True:
                try:
                    #* Window
                    windowCaptchaOneRegion = Box(window.left + 85, window.top + 150, 185, 70)
                    windowCaptchaTwoRegion = Box(window.left + 75, window.top + 120, 420, 140)
                    windowSliderRegion = Box(window.left, window.top + 350, 520, 80)
                    
                    #* Slider
                    captchaButton = pyautogui.locateOnScreen("./images/captcha_button.png", region=windowSliderRegion, confidence = 0.9)
                    buttonX, buttonY = pyautogui.center(captchaButton)
                    sliderMargin = buttonX - window.left
                    sliderSize = 520 - sliderMargin * 2

                    #* Captcha locate
                    first, second, third = self.find_captcha(windowCaptchaOneRegion)
                    self.bot_log.info(f"Trying find CAPTCHA: {first}{second}{third}")

                    #* Calculate scrolled distance, click and move
                    sliderDistance = int(sliderSize / 4)
                    buttonX, buttonY = self.randon_center(captchaButton, range = 0.1)                    
                    pyautogui.moveTo(buttonX, buttonY)
                    pyautogui.mouseDown()
                    for i in range(5):
                        if (i == 1):
                            pyautogui.move(-sliderDistance, self.randonMove(0, 4), self.randomRangeDecimal(1, 0.2), pyautogui.easeInOutQuad)
                        elif (i == 2):
                            pyautogui.move(sliderDistance * 2, self.randonMove(0, 4), self.randomRangeDecimal(1, 0.2), pyautogui.easeInOutQuad)
                        else:
                            pyautogui.move(sliderDistance, self.randonMove(0, 4), self.randomRangeDecimal(1, 0.2), pyautogui.easeInOutQuad)
                        if (self.find_captcha_two(windowCaptchaTwoRegion, first, second, third, i)):
                            break
                    pyautogui.mouseUp()

                    if (not self.is_image_present("./images/captcha_button.png")):
                        self.bot_log.info("Trying to solve captcha END")
                        break
                except Exception as e:
                    self.bot_log.error(f"Error on try_captcha: {e}")
                    time.sleep(self.randonTime(self._small_time))

    def find_captcha(self, box: Box):
        self.bot_log.info("Trying find CAPTCHA")
        numbers = []
        count = 0
        
        for i in range(10):
            try:
                number = pyautogui.locateOnScreen(f"./images/{i}.png", region=box, confidence = 0.92)
                if (number != None): 
                    numbers.append((i, number.left))
                    count += 1
                    if (count == 3):
                        break
            except Exception as e:
                self.bot_log.error(f"Error on find_captcha: {e}")
                raise ValueError("Unable to find captcha")

        numbersOrderned = sorted(numbers, key=lambda elem: elem[1])
        return [elem[0] for elem in numbersOrderned]
    
    def find_captcha_two(self, ssRegion: Box, first, second, third, whileIndex):
        ss = pyautogui.screenshot(region=ssRegion)

        white = (255, 255, 255)
        brown = (186, 113, 86)
        numbersToFind = (first, second, third)
        numbers = (
            [0, 106, ([10, 0, white], [35, -90, white], [55, 0, white]), 71], #100%
            [1, 120, ([3, -110, white], [6, -110, white], [13, 8, white]), 20], #100%
            [2, 110, ([33, -100, white], [40, 10, white], [80, 18, white]), 85], #100%
            [3, 17, ([40, 13, white], [57, 79, white], [54, 87, white]), 70], #50%
            [4, 28, ([7, 0, white], [40, 90, white], [50, 0, white]), 60], #100#
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
        while marginX < ssRegion.width:
            try:
                marginY = numbers[numberToFind][1]
                pixels = numbers[numberToFind][2]
                nextNumberStart = numbers[numberToFind][3]
                
                if (ss.getpixel((marginX, marginY)) == white):
                    pixelWhiteSize += 1
                    if (pixelWhiteSize == numberMinSize):
                        marginX -= numberMinSize - 1
                        pixelWhiteSize = 0
                        
                        # ss.putpixel((marginX, marginY), (0, 128, 0))
                        localizedAllPixels = 0
                        for pixel in pixels:
                            pixX = pixel[0]
                            pixY = pixel[1]
                            color = pixel[2]
                            if (ss.getpixel((marginX + pixX, marginY + pixY)) == color): 
                                localizedAllPixels += 1
                            # ss.putpixel((marginX + pixX, marginY + pixY), (255, 0, 0))

                        if (localizedAllPixels == 3):
                            marginX = marginX + nextNumberStart
                        else:
                            self.bot_log.info(f"#{whileIndex + 1} not find: {numberToFind}")
                            # ss.save(f'my_screenshot_{whileIndex + 1}.png')
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
        # ss.save(f'my_screenshot_{whileIndex + 1}.png')
        return True

    def scroll_down(self):
        try:
            drag_bars = list(pyautogui.locateAllOnScreen("./images/hero-selection-drag-bar.png", confidence = 0.8))
            x, y = self.randon_center(drag_bars[len(drag_bars)-1])
            time.sleep(self.randonTime(self._minimum_time))
            pyautogui.moveTo(x, y)
            time.sleep(self.randonTime(self._minimum_time))
            pyautogui.dragTo(x, random.randint(y-300, y-180), self.randonTime(self._minimum_time), button='left')
            return True
        except Exception as e:
            return False

    def put_heroes_to_work(self):
        self.bot_log.info("Trying put heroes to work")
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
                self.bot_log.error("Unable to go back to menu")
                continue

            if(not self.is_image_present("./images/hero-selection-drag-bar.png")):
                flag = self.await_and_click("./images/heroes-menu-button.png", self.randonTime(self._big_time))
            if(not flag):
                self.bot_log.error("heroes-menu-button.png not found")
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
                self.bot_log.error("Unable to go back to menu after putting heroes to work")
                continue

            puted_heroes_to_work = True

        if(not puted_heroes_to_work):
            raise ValueError("Unable to put heroes to work")

    def reset_map(self):
        self.bot_log.info("Redistributing heroes")
        self.await_and_click("./images/back-to-menu-button.png", self.randonTime(self._small_time))
        time.sleep(self.randonTime(self._small_time))
        self.await_and_click("./images/start-pve-button.png", self.randonTime(self._small_time))

    def await_for_new_map(self, await_time, map_expected_time_finish):
        self.bot_log.info(f"Awaiting {str(int(await_time / 60))}m for new map")

        time_left = await_time
        while time_left > 0:
            time_start = time.perf_counter()

            if(self.await_and_click("./images/new-map-button.png", self.randonTime(self._medium_time/2))):
                self.bot_log.info(f"Map time spent {str(int(map_time_spent / 60))}m")
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
                    # self.try_captcha()
                    self.refresh()
                    self.await_for_image("./images/connect-wallet-button.png", self._big_time)
                    self.try_to_login()
                elif(state == 2):
                    self.put_heroes_to_work()
                else:
                    self.await_for_new_map(self._data['map_time'], self._data['map_expected_time_finish'])
            except Exception as e:
                self.bot_log.error(f"Error during workflow: {e}")
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
        # bot.bot_log.error(f"Bot breaking error: {e}")
