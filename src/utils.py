import time
import random
import pyautogui
from pyautogui import *
from pyscreeze import Box

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

    def random_range_decimal(self, time, range = 0.25):
        time += random.uniform(time*range, time*range)
        return time

    def randon_time(self, time, range = 0.15):
        time += random.randint(-int(time*range), int(time*range))
        return time

    def random_position(self, position, range = 5):
        position += random.randint(-int(range), int(range))
        return position

    def random_time(self, time, range = 0.15):
        time += random.randint(-int(time*range), int(time*range))
        return time

    def randon_center(self, box, range = 0.25):
        el_with = box.width
        el_height = box.height
        x, y = pyautogui.center(box)
        x +=  random.randint(-int(el_with*range), int(el_with*range))
        y +=  random.randint(-int(el_height*range), int(el_height*range))
        return x, y

    def is_time_out(self, time_start, await_time):
        time_spent = time.perf_counter() - time_start
        return True if time_spent >= await_time else False

    def time_spent(self, time_start):
        return  time.perf_counter() - time_start

    def await_and_click(self, image, await_time, confidence = None, tag = "Image"):
        confidence = self._default_confidence if confidence == None else confidence
        self._log.debug(f"Await and click: {image} for {str(await_time)}s")

        time.sleep(self._minimum_time)
        time_start = time.perf_counter()

        while (self.is_time_out(time_start, await_time) == False):
            box = pyautogui.locateOnScreen(image, confidence = confidence)
            if (box != None):
                x, y = self.random_moveTo(box)
                self.click(x, y)
                self._log.info(f"{tag} founded and clicked")
                return box
            else:
                time.sleep(2)

        self._log.debug(f"{tag} not founded")
 
        return None

    def await_for_image(self, image, await_time, region: Box = None, confidence = None, tag = "Image"):
        confidence = self._default_confidence if confidence == None else confidence
        self._log.debug(f"Awaiting {str(await_time)}s for {image}")
        time.sleep(self._minimum_time)
        time_start = time.perf_counter()

        while (self.is_time_out(time_start, await_time) == False):
            box = pyautogui.locateOnScreen(image, region=region, confidence = confidence)
            if (box != None):
                self._log.info(f"{tag} founded")
                return box
            else:
                time.sleep(2)

        self.random_sleep(self._small_time)
        self._log.debug(f"{tag} not founded")
        return None

    def is_image_present(self, image, confidence = None, tag = "Image"):
        confidence = self._default_confidence if confidence == None else confidence
        self._log.debug(f"Checking if image is present: {image}")
        time.sleep(self._minimum_time)
        if (pyautogui.locateOnScreen(image, confidence = confidence) != None):
            self._log.info(f"{tag} founded")
            return True
        else:
            self._log.debug(f"{tag} not founded")
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
                time.sleep(self.randon_time(self._minimum_time))
                if(enable_log):
                    self._log.info("Image founded")
                else:
                    self._log.debug("Image founded")
                return x, y
            except:
                time.sleep(1)
        time.sleep(self.randon_time(self._small_time))
        if(enable_log):
            self._log.warning("Image not founded")
        else:
            self._log.debug("Image not founded")
        return -1, -1