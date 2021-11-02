from pyautogui import *
import pyautogui
import time
import json

# TODO: Puxar a tela de sign na aws para frente antes de procurar pelo botão

class Bot:
    _data = {
        'speed': 1.0,
        'map_time': 900,
        'work_button_confidence': 0.9,
        'server_lagged': False,
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
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.press('r')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')

    def await_and_click(self, image, await_time, confidance = 0.9):
        await_time = int(await_time)
        print("Awating for image: " + image + " for " + str(await_time) +"s")
        for i in range(0, await_time*2):
            try:
                x1, y1 = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                time.sleep(self._minimum_time)
                pyautogui.click(x1, y1)
                i += await_time
                print("Image founded and clicked")
                return True
            except:
                time.sleep(1)
        time.sleep(self._small_time)
        raise ValueError("Image " + image + " not founded")

    def await_for_image(self, image, await_time, confidance = 0.9):
        await_time = int(await_time)
        print("Awating for image: " + image + " for " + str(await_time) +"s")
        for i in range(0, await_time*2):
            try:
                x1, y1 = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
                i += await_time
                print("Image founded")
                return True
            except:
                time.sleep(self._minimum_time)
        time.sleep(self._small_time)
        raise ValueError("Image " + image + " not founded")

    def is_image_present(self, image, confidance = 0.9):
        try:
            founded = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
            return True
        except:
            return False
        
    def try_to_login(self):
        i = 1
        print("Trying to log in")
        pyautogui.dragTo(10, 10)
        while(not self.is_image_present("./images/start-pve-button.png")):
            try:
                self.await_and_click("./images/connect-wallet-button.png", await_time = 10+self._medium_time)
                time.sleep(self._small_time)
                self.await_and_click("./images/metamask-fox.png", await_time = 10+self._medium_time)
                time.sleep(self._small_time)
                if(self._data['plataform'].lower() == 'windows'):
                    self.await_and_click("./images/sing-button-windows.png", await_time = 10+self._medium_time)
                    self.await_for_image("./images/start-pve-button.png", self._big_time)
                    i+=1
            except Exception as e:
                print(e)
                self.refresh()

            if(self._data['plataform'].lower() == 'linux'):
                try:
                    self.await_and_click("./images/sing-button-linux.png", await_time = 2*self._medium_time)
                    self.await_for_image("./images/start-pve-button.png", self._big_time)
                except: 
                    time.sleep(self._small_time)
                    if(self.is_image_present("./images/metamask_sign_tab.png")):     
                        self.await_and_click("./images/metamask_sign_tab.png", self._medium_time)
                        time.sleep(self._small_time)
                        pyautogui.click(300, 300)
                    else:
                        print("Metamask tab not founded")
                    time.sleep(self._small_time)
                    try:
                        self.await_and_click("./images/sing-button-linux.png", await_time = 2*self._medium_time)
                        self.await_for_image("./images/start-pve-button.png", self._big_time)
                    except Exception as e:
                        print(e)
                        self.refresh()

        print("Logged in after " + str(i-1) +" attempts")

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
            raise ValueError("Unable to drag down")

    def put_heroes_to_work(self):
        time.sleep(self._medium_time)
        
        try:
            if(self.is_image_present("./images/back-to-menu-button.png")):
                self.await_and_click("./images/back-to-menu-button.png", self._medium_time)
            elif(self.is_image_present("./images/close-button.png")):
                self.await_and_click("./images/close-button.png", self._medium_time)
        except Exception as e:
            print(e)

        try:
            self.await_and_click("./images/heroes-menu-button.png", self._big_time)
        except:
            raise ValueError("heroes-menu-button.png not found")
        
        try:
            self.await_for_image("./images/hero-selection-drag-bar.png", self._big_time)
            for i in range(0,4):
                self.scroll_down()
        except Exception as e:
            print(e)
        time.sleep(self._small_time)
        work_buttons = list(pyautogui.locateAllOnScreen('./images/work-button.png', confidence = self._data['work_button_confidence']))
        if(len(work_buttons) > 0):
            x1, y1 = pyautogui.center(work_buttons[len(work_buttons)-1])
            for i in range(0, 20):
                pyautogui.click(x1, y1)
                time.sleep(self._small_time)
                if(not self.is_image_present('./images/work-button.png', confidance=0.5)):
                    self.await_and_click("./images/close-button.png", self._medium_time)
                    time.sleep(self._small_time)
                elif(not self.is_image_present('./images/work-button.png')):
                    break
        try:
            self.await_and_click("./images/close-button.png", 10)
            self.await_and_click("./images/start-pve-button.png", 10)
        except:
            raise ValueError("Erro whyle going back to pve")

    def await_for_new_map(self, await_time):
        print("Awaiting "+ str(await_time) +"s for new map")
        await_time = int(await_time/(self._small_time*2))
        for i in range(0, await_time):
            if(self.is_image_present('./images/ok-button.png')):
                raise ValueError("Lost connection")
            try:
                x1, y1 = pyautogui.center(pyautogui.locateOnScreen("./images/new-map-button.png", confidence = 0.9))
                pyautogui.click(x1, y1)
                i += await_time
                print("Image founded and clicked")
                print("Awaiting "+ str((await_time-i)) +"s for new map")
            except:
                time.sleep(self._small_time*2)

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
                print(e)
                self.refresh()
                self.await_for_image("./images/connect-wallet-button.png", self._big_time)
                self.try_to_login()
                state = 1

Bot().run()