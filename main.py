from playwright.sync_api import sync_playwright
from time import sleep
import os
import numpy as np
from PIL import Image
from PIL import ImageChops
import random
import requests
import sys
import yaml

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage?chat_id={chat_id}&text={message}"
    return requests.get(url).json()

def clear_screenshots():
    if os.path.exists("/tmp/screenshot.png"):
        os.remove("/tmp/screenshot.png")
    if os.path.exists("/tmp/screenshot_prev.png"):
        os.remove("/tmp/screenshot_prev.png")

def pause_random(start, end):
    rest_int = random.randint(start, end)
    print(f"Pausing for {rest_int} seconds..")
    sleep(rest_int)

def detect_change():
    if os.path.exists("/tmp/screenshot_prev.png"):
        screenshot_prev = Image.open("/tmp/screenshot_prev.png")
        screenshot = Image.open("/tmp/screenshot.png") 
        diff = ImageChops.difference(screenshot, screenshot_prev)
        diff_val = np.sum(np.asarray(diff))
    else:
        diff_val = 0
    return diff_val

def update_screenshots(page):
    if os.path.exists("/tmp/screenshot.png"):
        os.rename("/tmp/screenshot.png", "/tmp/screenshot_prev.png")
    page.screenshot(path="/tmp/screenshot.png", full_page=True)

# Load config
CONFIG_PATH = sys.argv[1]
with open(CONFIG_PATH) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
TELEGRAM_API_KEY = config["TELEGRAM_API_KEY"]

# Get ChatID from Telegram
url = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/getUpdates"
response = requests.get(url).json()
while True:
    chat_ids = set(x['message']['from']['id'] for x in response['result'])
    if len(chat_ids) == 0:
        input("Send a Telegram message to the bot, then press Enter")
    break

if len(chat_ids) == 1:
    chat_id = chat_ids.pop()
else:
    print(chat_ids)
    chat_id = input("Multiple IDs found, enter chat ID: ")

send_telegram_message("Let's start!")

# Run refresh loop
with sync_playwright() as p:
    clear_screenshots()

    # Go to first login page
    browser = p.firefox.launch(headless=False, devtools=True)
    page = browser.new_page()
    page.goto(config["FIRST_LOGIN_PAGE"])

    input("Press ENTER to refresh on loop...")
    while True:
        for i in range(5):
            page.reload()
            pause_random(10, 30)

            update_screenshots(page)

            if detect_change() > 0:
                send_telegram_message(f"Page Changed. {config['FIRST_LOGIN_PAGE']}")
                input("Pausing reload, press enter to continue")
                clear_screenshots()

        # print("Switching to ALT_LOGIN_PAGE..")
        # page.goto(config["ALT_LOGIN_PAGE"])
        # pause_random(10, 15)
        # sleep(random.randint(10, 15))
        pause_random(3, 5)
