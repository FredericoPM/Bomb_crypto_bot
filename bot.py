from numpy import true_divide
from pyautogui import *
import pyautogui
import time
import json

class Bot:
    _data = {
        'speed': 1.0,
        'map_time': 900,
        'work_button_confidence': 0.9,
        'default_confidence': 0.9,
        'put_to_work_trys': 45,
        'plataform': 'windows'
    }

    _minimum_time = 0.5
    _small_time = 1
    _medium_time = 5
    _big_time = 20
    
    def __init__(self, config_file = "config.json"):
        config_file = config_file if config_file.find(".json") != -1 else "config.json"
        try:
            with open(config_file, "r") as read_file:
                self._data = json.load(read_file)
        except Exception as e:
            with open(config_file, "w") as write_file:
                json.dump(self._data, write_file,indent=2)

        self._data['speed'] = 1 if self._data['speed'] > 1 else self._data['speed']
        self._minimum_time *= (1/self._data['speed'])
        self._small_time *= (1/self._data['speed'])
        self._medium_time *= (1/self._data['speed'])
        self._big_time *= (1/self._data['speed'])

    def refresh(self):
        #print("refreshing page")
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')


    def await_and_click(self, image, await_time, confidance = _data['default_confidence']):
        await_time = int(await_time/2)
        await_time = await_time if await_time > 1 else 2
        #print("Awating for image: " + image + " for " + str(await_time*2) +"s")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                time.sleep(self._minimum_time)
                pyautogui.click(x, y)
                #print("Image founded and clicked")
                return True
            except:
                time.sleep(2)
        time.sleep(self._small_time)
        return False

    def search_for(self, image, await_time, confidance = _data['default_confidence']):
        await_time = int(await_time)
        #print("Awating for image: " + image + " for " + str(await_time) +"s")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                time.sleep(self._minimum_time)
                #print("Image founded")
                return x, y
            except:
                time.sleep(1)
        time.sleep(self._small_time)
        return False

    def await_for_image(self, image, await_time, confidance = 0.9):
        await_time = int(await_time/2)
        await_time = await_time if await_time > 1 else 2
        #print("Awating for image: " + image + " for " + str(await_time*2) +"s")
        for i in range(0, await_time):
            try:
                x1, y1 = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                i += await_time
                #print("Image founded")
                return True
            except:
                time.sleep(2)
        time.sleep(self._small_time)
        return False
    
    def is_image_present(self, image, confidance = 0.9):
        try:
            founded = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
            return True
        except:
            return False

    def try_to_login(self):
        i = 1
        #print("Trying to log in")
        pyautogui.dragTo(100, 100)
        while(not self.is_image_present("./images/start-pve-button.png")):

            flag = self.await_and_click("./images/connect-wallet-button.png", await_time = 3*self._medium_time)
            time.sleep(self._small_time)
            flag = flag and self.await_and_click("./images/metamask-fox.png", await_time = 3*self._medium_time)
            time.sleep(self._small_time)
            if(not flag):
                #print("Error while trying to connect")
                self.refresh()
                continue

            if(self._data['plataform'].lower() == 'windows'):
                flag = self.await_and_click("./images/sing-button-windows.png", await_time = 3*self._medium_time)
                if(not flag):
                    #print("Error while trying to connect")
                    self.refresh()
                    continue
            else:
                flag = self.await_and_click("./images/sing-button-linux.png", await_time = self._medium_time)
                if(not flag):
                    try:
                        x, y = self.search_for("./images/metamask_sign_tab.png", await_time = 2*self._medium_time)
                        pyautogui.click(x, y)
                        time.sleep(self._small_time)
                        self.await_and_click("./images/sing-button-linux.png", await_time = 2*self._medium_time)
                        time.sleep(self._small_time)
                        pyautogui.click(x, y)
                        time.sleep(self._small_time)
                    except Exception as e:
                        #print(e)
                        self.refresh()
                        continue

            flag = self.await_for_image("./images/start-pve-button.png", self._big_time)
            i+=1
            if(not flag):
                #print("start-pve-button not founded")
                self.refresh()
                continue

        #print("Logged in after " + str(i-1) +" attempts")

    def scroll_down(self):
        try:
            drag_bars = list(pyautogui.locateAllOnScreen("./images/hero-selection-drag-bar.png", confidence = 0.8))
            x1, y1 = pyautogui.center(drag_bars[len(drag_bars)-1])
            time.sleep(self._minimum_time)
            pyautogui.dragTo(x1, y1)
            time.sleep(self._minimum_time)
            pyautogui.dragTo(x1, y1-200, self._minimum_time, button='left')
            return True
        except Exception as e:
            return False

    def put_heroes_to_work(self):
        time.sleep(self._medium_time)

        puted_heroes_to_work = False
        flag = True
        for i in range (0,5):
            if(puted_heroes_to_work):
                continue

            if(self.is_image_present("./images/back-to-menu-button.png") and not self.is_image_present("./images/hero-selection-drag-bar.png")):
                flag = self.await_and_click("./images/back-to-menu-button.png", self._big_time)
            elif(self.is_image_present("./images/close-button.png")):
                flag = self.await_and_click("./images/close-button.png", self._big_time)
            if(not flag):
                #print("Unable to go back to menu")
                continue
            time.sleep(self._small_time)

            if(not self.is_image_present("./images/hero-selection-drag-bar.png")):
                flag = self.await_and_click("./images/heroes-menu-button.png", self._big_time)
            if(not flag):
                #print("heroes-menu-button.png not found")
                continue
            time.sleep(self._small_time)

            self.await_for_image("./images/hero-selection-drag-bar.png", self._big_time)
            for i in range(0,4):
                flag = self.scroll_down()
                i = i-1 if not flag else i
            time.sleep(self._small_time)

            work_buttons = list(pyautogui.locateAllOnScreen('./images/work-button.png', confidence = self._data['work_button_confidence']))
            if(len(work_buttons) > 0):
                x1, y1 = pyautogui.center(work_buttons[len(work_buttons)-1])
                for i in range(0, self._data['put_to_work_trys']):
                    pyautogui.click(x1, y1)
                    time.sleep(self._small_time)
                    if(not self.is_image_present('./images/work-button.png', confidance=0.5)):
                        self.await_and_click("./images/close-button.png", self._medium_time)
                        time.sleep(self._small_time)
                    elif(not self.is_image_present('./images/work-button.png')):
                        break
            
            flag = self.await_and_click("./images/close-button.png", 2*self._medium_time)
            flag = self.await_and_click("./images/start-pve-button.png", 2*self._medium_time)
            if(not flag):
                #print("Unable to go back to menu")
                continue

            puted_heroes_to_work = True

        if(not puted_heroes_to_work):
            raise ValueError("Unable to put heroes to work")

    def reset_map(self):
        flag = self.await_and_click("./images/back-to-menu-button.png", self._medium_time)
        time.sleep(self._small_time*2)
        flag = self.await_and_click("./images/start-pve-button.png", self._medium_time)

        if(not flag):
            raise ValueError("Unable to reset map")
    
    def await_for_new_map(self, await_time):
        #print("Awaiting "+ str(await_time) +"s for new map")
        await_time = int(await_time/self._medium_time)

        for i in range(0, await_time):
            self.await_and_click("./images/new-map-button.png", self._medium_time/2)
            if(self.await_and_click("./images/ok-button.png", self._medium_time/2)):
                raise ValueError("Lost connection")
            if(i*self._medium_time > 900 and int(i*self._medium_time) % 60 == 0):
                self.reset_map()

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
            time.sleep(self._small_time)
            state = self.select_wat_to_do(state)
            try:
                if(state == 1):
                    self.refresh()
                    self.await_for_image("./images/connect-wallet-button.png", self._big_time)
                    self.try_to_login()
                elif(state == 2):
                    self.put_heroes_to_work()
                else:
                    self.await_for_new_map(self._data['map_time'])
            except Exception as e:
                #print(e)
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
        #print(e)