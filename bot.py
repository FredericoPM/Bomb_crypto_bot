from os import error
from numpy import logical_not, minimum
from pyautogui import *
import pyautogui
import time

speed = 1
minimum_time = 0.5 * (1/speed)
small_time = 1 * (1/speed)
medium_time = 5 * (1/speed)
big_time = 20 * (1/speed)

def refresh():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    pyautogui.press('r')
    pyautogui.keyUp('shift')
    pyautogui.keyUp('ctrl')
    time.sleep(small_time)

def await_and_click(image, await_time, confidance = 0.9):
    await_time = int(await_time)
    print("Awating for image: " + image + " for " + str(await_time) +"s")
    for i in range(0, await_time*2):
        try:
            x1, y1 = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
            time.sleep(minimum_time)
            pyautogui.click(x1, y1)
            i += await_time
            print("Image founded and clicked")
            return True
        except:
            time.sleep(1)
    
    raise ValueError("Image " + image + " not founded")

def await_for_image(image, await_time, confidance = 0.9):
    await_time = int(await_time)
    print("Awating for image: " + image + " for " + str(await_time) +"s")
    for i in range(0, await_time*2):
        try:
            x1, y1 = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
            i += await_time
            print("Image founded")
            return True
        except:
            time.sleep(minimum_time)
    
    raise ValueError("Image " + image + " not founded")

def find_and_click(image, confidance = 0.9):
    print("Trying to click on: " + image)
    try:
        x1, y1 = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
        time.sleep(minimum_time)
        pyautogui.click(x1, y1)
        print("Image founded and clicked")
        return True
    except:
        raise ValueError("Image " + image + " not founded")

def is_image_present(image, confidance = 0.9):
    try:
        founded = pyautogui.center(pyautogui.locateOnScreen(image, confidence = confidance))
        return True
    except:
        return False
    
def try_to_login():
    i = 1
    print("Trying to log in")
    pyautogui.dragTo(10, 10)
    while(not is_image_present("./images/start-pve-button.png")):
        try:
            await_and_click("./images/connect-wallet-button.png", await_time = 10+medium_time)
            await_and_click("./images/metamask-fox.png", await_time = 10+medium_time)
            await_and_click("./images/assinar-button.png", await_time = 10+medium_time)
            await_for_image("./images/start-pve-button.png", big_time)
            i+=1
        except Exception as e:
            print(e)
            refresh()
    print("Logged in after " + str(i-1) +" attempts")

def scroll_down():
    try:
        drag_bars = list(pyautogui.locateAllOnScreen("./images/hero-selection-drag-bar.png", confidence = 0.8))
        x1, y1 = pyautogui.center(drag_bars[len(drag_bars)-1])
        time.sleep(minimum_time)
        pyautogui.dragTo(x1, y1)
        time.sleep(minimum_time)
        pyautogui.dragTo(x1, y1-200, minimum_time, button='left')
        return True
    except Exception as e:
        raise ValueError("Unable to drag down")

def put_heroes_to_work():
    time.sleep(medium_time)
    
    try:
        if(is_image_present("./images/back-to-menu-button.png")):
            find_and_click("./images/back-to-menu-button.png")
        elif(is_image_present("./images/close-button.png")):
            find_and_click("./images/close-button.png")
    except Exception as e:
        print(e)

    try:
        await_and_click("./images/heroes-menu-button.png", 30)
    except:
        raise ValueError("heroes-menu-button.png not found")
    
    try:
        await_for_image("./images/hero-selection-drag-bar.png", 30)
        for i in range(0,4):
            scroll_down()
    except Exception as e:
        print(e)
    time.sleep(small_time)
    work_buttons = list(pyautogui.locateAllOnScreen('./images/work-button.png', confidence = 0.9))
    if(len(work_buttons) > 0):
        x1, y1 = pyautogui.center(work_buttons[len(work_buttons)-1])
        for i in range(0, 20):
            pyautogui.click(x1, y1)
            time.sleep(small_time)
            if(not is_image_present('./images/work-button.png', confidance=0.5)):
                find_and_click("./images/close-button.png")
            elif(not is_image_present('./images/work-button.png')):
                break
    try:
        await_and_click("./images/close-button.png", 10)
        await_and_click("./images/start-pve-button.png", 10)
    except:
        raise ValueError("Erro whyle going back to pve")

def await_for_new_map(await_time):
    print("Awaiting "+ str(await_time) +"s for new map")
    await_time = int(await_time)
    for i in range(0, await_time):
        if(is_image_present('./images/ok-button.png')):
            raise ValueError("Lost connection")
        try:
            x1, y1 = pyautogui.center(pyautogui.locateOnScreen("./images/new-map-button.png", confidence = 0.9))
            pyautogui.click(x1, y1)
            i += await_time
            print("Image founded and clicked")
            print("Awaiting "+ str((await_time-i)) +"s for new map")
        except:
            time.sleep(1)

#* 1 - login
#* 2 - Put heroes to work
#* 3 - Await for a new map
def select_wat_to_do(last_action):
    if(last_action == 0 and not is_image_present("./images/start-pve-button.png") and not is_image_present("./images/back-to-menu-button.png") and not is_image_present("./images/close-button.png")):
        return 1
    elif(last_action == 0 or last_action == 1 or last_action == 3):
        return 2
    elif(last_action == 2 and is_image_present("./images/back-to-menu-button.png")):
        return 3
    else:
        return 1

estado = 0
while 1:
    time.sleep(small_time)
    estado = select_wat_to_do(estado)
    try:
        if(estado == 1):
            refresh()
            await_for_image("./images/connect-wallet-button.png", big_time)
            try_to_login()
        elif(estado == 2):
            put_heroes_to_work()
        else:
            await_for_new_map(900)
    except Exception as e:
        print(e)
        refresh()
        await_for_image("./images/connect-wallet-button.png", big_time)
        try_to_login()
        estado = 1
    
