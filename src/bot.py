import time
import random
import pyautogui
from pyautogui import *
from pyscreeze import Box

class Bot:
    _data = None
    _bot_log = None
    _minimum_time = None
    _small_time = None
    _medium_time = None
    _big_time = None
    _utils = None

    _map_time_start = time.perf_counter()

    def __init__(self, data, log, minimum_time, small_time, medium_time, big_time, utils):
        pyautogui.FAILSAFE = False
        self._data = data
        self._bot_log = log
        self._minimum_time = minimum_time
        self._small_time = small_time
        self._medium_time = medium_time
        self._big_time = big_time
        self._utils = utils

    def refresh(self):
        self._bot_log.info("Refreshing page")
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')
        time.sleep(self._utils.randon_time(self._big_time))
    
    def try_to_login(self, trys = None):
        self._bot_log.info("Trying to login")
        self._utils.random_move(-300,  0)
        self._utils.random_sleep(self._small_time)

        attempts = 1
        while (not self._utils.is_image_present("./images/start-pve-button.png", tag = "PVE") and (trys == None or attempts <= trys)):

            if (self._utils.await_and_click("./images/connect-wallet-button.png", await_time = 2*self._medium_time, tag = "CONNECT") == None):
                self._bot_log.error("Error while trying connect")
                self.refresh()
                continue

            self.try_captcha()

            self._bot_log.info("Trying to sign metamask")
            if (self._data['plataform'].lower() == 'windows'):
                if (self._utils.await_and_click("./images/sing-button-windows.png", await_time = 2*self._medium_time, tag = "SIGN") == None):
                    self._bot_log.error("Error while trying to connect")
                    self.refresh()
                    continue
            else:
                if(self._data['browser'].lower() == 'vivald'):
                    box = self._utils.await_and_click("./images/sing-button-linux-vivald.png", await_time = 2*self._medium_time, tag = "SIGN")
                else:
                    box = self._utils.await_and_click("./images/sing-button-linux-chrome.png", await_time = 2*self._medium_time, tag = "SIGN")

                if(box == None):
                    try:
                        if(self._data['browser'].lower() == 'vivald'):
                            x, y = self._utils.search_for("./images/metamask_sign_tab_vivald.png", await_time = self._utils.randon_time(2*self._medium_time))
                        else:
                            x, y = self._utils.search_for("./images/metamask_sign_tab_chrome.png", await_time = self._utils.randon_time(*self._medium_time))
                        if(x == -1):
                            raise ValueError("metamask_sign_tab not founded")
                        pyautogui.click(x, y)
                        time.sleep(self._utils.randon_time(self._small_time))
                        if(self._data['browser'].lower() == 'vivald'):
                            flag = self._utils.await_and_click("./images/sing-button-linux-vivald.png", await_time = self._utils.randon_time(2*self._medium_time))
                        else:
                            flag = self._utils.await_and_click("./images/sing-button-linux-chrome.png", await_time = self._utils.randon_time(2*self._medium_time))
                        time.sleep(self._utils.randon_time(self._small_time))
                        pyautogui.click(x, y)
                        time.sleep(self._utils.randon_time(self._small_time))
                    except Exception as e:
                        self._bot_log.error(f"Error while trying to connect: {e}")
                        self.refresh()
                        continue

            attempts += 1
            if (self._utils.await_for_image("./images/start-pve-button.png", await_time = 5*self._big_time, tag = "PVE") == None):
                self._bot_log.error("Error while trying connect")
                self.refresh()
                continue

        self._bot_log.info(f"Logged in after {str(attempts-1)} attempts")
        
    def try_captcha(self):
        window = self._utils.await_for_image("./images/captcha_window.png", await_time = self._minimum_time, confidence = 0.92, tag = "WINDOW")
        if (window != None):
            self._bot_log.info("Captcha START")
            try:
                while True:
                    #* Window
                    windowCaptchaOneRegion = Box(window.left + 85, window.top + 150, 185, 70)
                    windowCaptchaTwoRegion = Box(window.left + 75, window.top + 120, 420, 140)
                    windowSliderRegion = Box(window.left, window.top + 350, 520, 80)

                    #* Slider
                    captchaButton = self._utils.await_for_image("./images/captcha_button.png", await_time = self._small_time, region = windowSliderRegion, tag = "SLIDER")
                    buttonX, buttonY = pyautogui.center(captchaButton)
                    sliderMargin = buttonX - window.left
                    sliderSize = 520 - sliderMargin * 2

                    #* Captcha locate
                    first, second, third = self.find_captcha(windowCaptchaOneRegion)
                    self._bot_log.info(f"Trying find captcha: {first}{second}{third}")

                    #* Calculate scrolled distance, click and move
                    self._utils.random_moveTo(captchaButton, range = 0.1)
                    sliderDistance = int(sliderSize / 4)

                    pyautogui.mouseDown()
                    for i in range(5):
                        if (i == 1):
                            self._utils.random_move(-sliderDistance, 0, time = 0.7)
                        elif (i == 2):
                            self._utils.random_move(sliderDistance * 2, 0, time = 0.7)
                        else:
                            self._utils.random_move(sliderDistance, 0, time = 0.7)
                        if (self.find_captcha_two(windowCaptchaTwoRegion, first, second, third, i)):
                            break
                    pyautogui.mouseUp()

                    if (not self._utils.is_image_present("./images/captcha_button.png", tag = "SLIDER")):                        
                        self._bot_log.info("Captcha END")
                        break
            except Exception as e:
                self._bot_log.error(f"Error on try_captcha: {e}")
                raise ValueError("Unable to Try Captcha")

    def find_captcha(self, box: Box):
        self._bot_log.info("Trying find captcha")
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
            self._bot_log.error(f"Error on find_captcha: {e}")
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
                                self._bot_log.info(f"#{whileIndex + 1} not find: {numberToFind}")
                                # ss.save(f'my_screenshot_{whileIndex + 1}.png')
                                return False

                            numberPosition += 1
                            if (numberPosition < 3):
                                numberToFind = numbersToFind[numberPosition]
                            else:
                                self._bot_log.info(f"#{whileIndex + 1} find all")
                    else:
                        pixelWhiteSize = 0

                    marginX += 1
                except Exception as e:
                    print(e)
                    return False
            # ss.save(f'my_screenshot_{whileIndex + 1}.png')
            return True
        except Exception as e:
            self._bot_log.error(f"Error on find_captcha_two: {e}")
            raise ValueError("Unable to Find Captcha Two")

    def scroll_down(self):
        try:
            drag_bars = list(pyautogui.locateAllOnScreen("./images/hero-selection-drag-bar.png", confidence = 0.8))
            drag = drag_bars[len(drag_bars)-1]
            self._utils.random_moveTo(drag)
            self._utils.random_drag(0, -220, time = 0.4)
            self._utils.random_sleep(self._minimum_time)
            return True
        except Exception as e:
            self._bot_log.error(f"Error on scroll_down: {e}")
            return False

    def put_heroes_to_work(self):
        self._bot_log.info("Trying put heroes to work")
        self._utils.random_sleep(self._medium_time)

        puted_heroes_to_work = False
        stopFlow = False

        for i in range (5):

            #* PVE screen
            if (self._utils.is_image_present("./images/back-to-menu-button.png", tag = "BACK") and not self._utils.is_image_present("./images/hero-selection-drag-bar.png", tag = "HERO")):
                stopFlow = self._utils.await_and_click("./images/back-to-menu-button.png", await_time = self._big_time, tag = "BACK") == None
            #* Heroes screen
            elif (self._utils.is_image_present("./images/close-button.png", tag = "CLOSE")):
                stopFlow = self._utils.await_and_click("./images/close-button.png", await_time = self._big_time, tag = "CLOSE") == None

            if (stopFlow):
                self._bot_log.error("Unable to go back to menu")
                continue

            #* Menu screen
            if (not self._utils.is_image_present("./images/hero-selection-drag-bar.png", tag = "HERO")):
                stopFlow = self._utils.await_and_click("./images/heroes-menu-button.png", await_time = self._big_time, tag = "HEROES") == None
            if (stopFlow):
                self._bot_log.error("heroes-menu-button.png not found")
                continue

            self.try_captcha()

            self._utils.await_for_image("./images/hero-selection-drag-bar.png", await_time = self._big_time, tag = "HERO")

            if (self._utils.await_and_click("./images/ok-button.png", await_time = self._small_time, tag = "OK")):
                self._utils.random_sleep(self._medium_time)
                return

            for i in range(3):
                flag = self.scroll_down()
                i = i-1 if not flag else i
            
            self._bot_log.info("Searching for clickable work buttons")
            work_buttons = list(pyautogui.locateAllOnScreen('./images/work-button.png', confidence = self._data['work_button_confidence']))
            self._bot_log.info(f"{len(work_buttons)} clickable work buttons founded")
            
            self._bot_log.info("Putting heroes to work")
            if (len(work_buttons) > 0):
                box = work_buttons[len(work_buttons)-1]
                x, y = self._utils.random_moveTo(box)

                for i in range(0, self._data['put_to_work_trys']):
                    self._utils.click(x, y)
                    if (not self._utils.is_image_present('./images/work-button.png', confidence = 0.5, tag = "WORK")):
                        self._utils.await_and_click("./images/close-button.png", await_time = self._medium_time, tag = "CLOSE")
                    elif (not self._utils.is_image_present('./images/work-button.png', confidence = self._data['work_button_confidence'], tag = "WORK")):
                        break

            stopFlow = self._utils.await_and_click("./images/close-button.png", await_time = 2*self._medium_time, tag = "CLOSE") == None
            stopFlow = self._utils.await_and_click("./images/start-pve-button.png", await_time = 2*self._medium_time, tag = "PVE") == None

            if (stopFlow):
                self._bot_log.error("Unable to go back to menu after putting heroes to work")
                continue

            self._bot_log.info("Done putting heroes to work")
            puted_heroes_to_work = True
            break

        if (not puted_heroes_to_work):
            raise ValueError("Unable to put heroes to work")

    def reset_map(self):
        self._bot_log.info("Redistributing heroes")
        self._utils.await_and_click("./images/back-to-menu-button.png", self._small_time, tag = "BACK")
        self._utils.await_and_click("./images/start-pve-button.png", self._small_time, tag = "PVE")

    def await_for_new_map(self, await_time, map_expected_time_finish):
        self.bot_log.info(f"Awaiting {str(int(await_time / 60))}m for new map")
        time_left = await_time
        
        while time_left > 0:
            time_start = time.perf_counter()

            if(self._utils.await_and_click("./images/new-map-button.png", self._utils.randon_time(self._medium_time/2))):
                self.bot_log.info(f"Map time spent {str(int(map_time_spent / 60))}m")
                self._map_time_start = time.perf_counter()
                self.try_captcha()

            if(self._utils.await_for_image("./images/connect-wallet-button.png", self._medium_time/2)):
                raise ValueError("Captcha failed after 3 attempts")

            if(self._utils.is_image_present("./images/ok-button.png")):
                self.refresh()
                self._utils.await_for_image("./images/connect-wallet-button.png", self._big_time)
                self.try_to_login()
                self._utils.await_and_click("./images/start-pve-button.png", self._utils.randon_time(2*self._medium_time))

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
        if(last_action == 0 and not self._utils.is_image_present("./images/start-pve-button.png", tag = "PVE") and not self._utils.is_image_present("./images/back-to-menu-button.png", tag = "BACK") and not self._utils.is_image_present("./images/close-button.png", tag = "CLOSE")):
            return 1
        elif(last_action == 0 or last_action == 1 or last_action == 3):
            return 2
        elif(last_action == 2 and self._utils.is_image_present("./images/back-to-menu-button.png", tag = "BACK")):
            return 3
        else:
            return 1

    def run(self):
        state = 0

        while True:
            random.seed(time.time())
            self._utils.random_sleep(self._medium_time)
            state = self.select_wat_to_do(state)
            try:
                if(state == 1):
                    self.refresh()
                    self._utils.await_for_image("./images/connect-wallet-button.png", await_time = self._big_time, tag = "CONNECT")
                    self.try_to_login()
                elif(state == 2):
                    self.put_heroes_to_work()
                else:
                    self.await_for_new_map(self._data['map_time'], self._data['map_expected_time_finish'])
            except Exception as e:
                self._bot_log.error(f"Workflow was broken: {e}")
                self.refresh()
                self._utils.await_for_image("./images/connect-wallet-button.png", await_time = self._big_time, tag = "CONNECT")
                self.try_to_login()
                state = 1