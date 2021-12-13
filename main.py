import json
import logging
from src.bot import Bot
from src.utils import Utils
from src.multi_bot import Multi_bot
from logging.handlers import RotatingFileHandler

def read_config(config_file = "config.json"):
    data = {
        'speed': 1.0,
        'map_time': 2400,
        'map_expected_time_finish': 9000,
        'work_button_confidence': 0.92,
        'default_confidence': 0.92,
        'put_to_work_trys': 45,
        'plataform': 'windows',
        'browser': 'chrome',
        "console_log": True,
        "log_level": "info"
    }
    config_file = config_file if config_file.find(".json") != -1 else "config.json"
    try:
        with open(config_file, "r") as read_file:
            data = json.load(read_file)
    except Exception as e:
        with open(config_file, "w") as write_file:
            json.dump(data, write_file, indent=2)

    data['speed'] = 1 if data['speed'] > 1 else data['speed']

    return data

data = read_config()
minimum_time = 0.5 * (1/data['speed'])
small_time = 1 * (1/data['speed'])
medium_time = 5 * (1/data['speed'])
big_time = 20 * (1/data['speed'])

if(data['console_log']):
    log = logging
    log.basicConfig(format ='[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S', level = logging.DEBUG if data['log_level'].lower() == "debug" else logging.INFO)
else:
    log_formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    my_handler = RotatingFileHandler('./.log', mode='a', maxBytes=1024*1024, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.DEBUG if data['log_level'].lower() == "debug" else logging.INFO)
    log = logging.getLogger('root')
    log.setLevel(logging.DEBUG if data['log_level'].lower() == "debug" else logging.INFO)
    log.addHandler(my_handler)
    
if(data['number_of_bots'] > 1):
    multi_bot = Multi_bot(
        data,
        log,
        minimum_time, 
        small_time, 
        medium_time, 
        big_time, 
        Utils(log, minimum_time, small_time, medium_time, big_time, data['default_confidence']),
        "C:\Program Files\Google\Chrome\Application\chrome.exe"
    )
    while 1:
        try:
            multi_bot.run()
        except Exception as e:
            multi_bot = Multi_bot(
                data,
                log,
                minimum_time, 
                small_time, 
                medium_time, 
                big_time, 
                Utils(log, minimum_time, small_time, medium_time, big_time, data['default_confidence']),
                "C:\Program Files\Google\Chrome\Application\chrome.exe"
            )
            log.error(f"Bot breaking error: {e}")
else:
    bot = Bot(
            data, 
            log, 
            minimum_time, 
            small_time, 
            medium_time, 
            big_time, 
            Utils(log, minimum_time, small_time, medium_time, big_time, data['default_confidence'])
        )
    while 1:
        try:
            bot.run()
        except Exception as e:
            bot = Bot(
                data, 
                log, 
                minimum_time, 
                small_time, 
                medium_time, 
                big_time, 
                Utils(log, minimum_time, small_time, medium_time, big_time, data['default_confidence'])
            )
            log.error(f"Bot breaking error: {e}")

