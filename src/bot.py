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