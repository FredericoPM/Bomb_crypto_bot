import time
import random
import pyautogui
from pyautogui import *

class Utils:
    _minimum_time = 0.5
    _small_time = 1
    _medium_time = 5
    _big_time = 20
    _default_confidence = 0.92
    _log = None

    def __init__(self, log, minimum_time, small_time, medium_time, big_time, default_confidence):
        self._log = log
        self._minimum_time = minimum_time
        self._small_time = small_time
        self._medium_time = medium_time
        self._big_time = big_time
        self._default_confidence = default_confidence

    def randomRangeDecimal(self, value, range):
        return value + random.uniform(-range, range)

    def randonTime(self, time, range = 0.15):
        time += random.randint(-int(time*range), int(time*range))
        return time

    def randonMove(self, position, range = 2):
        position += random.randint(-int(position+range), int(position+range))
        return position

    def randon_center(self, box, range = 0.25):
        el_with = box.width
        el_height = box.height
        x, y = pyautogui.center(box)
        x +=  random.randint(-int(el_with*range), int(el_with*range))
        y +=  random.randint(-int(el_height*range), int(el_height*range))
        return x, y

    def await_and_click(self, image, await_time, confidence = None, enable_log = True):
        confidence = self._default_confidence if confidence == None else confidence

        await_time = int(await_time/2)
        await_time = await_time if await_time > 1 else 2
        if(enable_log):
            self._log.info(f"Await and click: {image} for {str(await_time*2)}s")
        else:
            self._log.debug(f"Await and click: {image} for {str(await_time*2)}s")

        for i in range(0, await_time):
            try:
                x, y = self.randon_center(pyautogui.locateOnScreen(image, confidence = confidence))
                pyautogui.moveTo(x, y)
                time.sleep(self.randonTime(self._minimum_time))
                pyautogui.click(x, y)
                if(enable_log):
                    self._log.info("Image founded and clicked")
                else:
                    self._log.debug("Image founded and clicked")
                return True
            except:
                time.sleep(2)
        time.sleep(self.randonTime(self._small_time))

        if(enable_log):
            self._log.warning("Image not founded")
        else:
            self._log.debug("Image not founded")

        return False

    def search_for(self, image, await_time, confidence = None, enable_log = True):
        confidence = self._default_confidence if confidence == None else confidence
        await_time = int(await_time)
        if(enable_log):
            self._log.info(f"Search for image: {image} for {str(await_time)}s")
        else:
            self._log.debug(f"Search for image: {image} for {str(await_time)}s")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidence))
                time.sleep(self.randonTime(self._minimum_time))
                if(enable_log):
                    self._log.info("Image founded")
                else:
                    self._log.debug("Image founded")
                return x, y
            except:
                time.sleep(1)
        time.sleep(self.randonTime(self._small_time))
        if(enable_log):
            self._log.warning("Image not founded")
        else:
            self._log.debug("Image not founded")
        return -1, -1

    def await_for_image(self, image, await_time, confidence = None, enable_log = True):
        confidence = self._default_confidence if confidence == None else confidence
        await_time = int(await_time/2)
        await_time = await_time if await_time > 1 else 2
        if(enable_log):
            self._log.info(f"Awaiting {str(await_time*2)}s for {image}")
        else:
            self._log.debug(f"Awaiting {str(await_time*2)}s for {image}")
        for i in range(0, await_time):
            try:
                x, y = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidence))
                i += await_time
                if(enable_log):
                    self._log.info("Image founded")
                else:
                    self._log.debug("Image founded")
                return True
            except:
                time.sleep(2)
        time.sleep(self.randonTime(self._small_time))
        if(enable_log):
            self._log.warning("Image not founded")
        else:
            self._log.debug("Image not founded")
        return False

    def is_image_present(self, image, confidence = None, enable_log = True):
        confidence = self._default_confidence if confidence == None else confidence
        if(enable_log):
            self._log.info(f"Checking if this image is present: {image}")
        else:
            self._log.debug(f"Checking if this image is present: {image}")
        time.sleep(self.randonTime(self._small_time))
        try:
            founded = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidence))
            if(enable_log):
                self._log.info(f"Image founded: {image}")
            else:
                self._log.debug(f"Image founded: {image}")
            return True
        except:
            if(enable_log):
                self._log.warning("Image not founded")
            else:
                self._log.debug("Image not founded")
            return False