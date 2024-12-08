# refresh-bot

A basic bot that:
1. Opens up a browser, allowing you to navigate to a particular page
2. Repeatedly refreshes the page
3. Takes a screenshot each time and compares them for any changes
4. Sends a telegram alert whenever a change is found.

Use it for a simple alert system to detect when a change happens on a website.

Tested on Raspiberry Pi running Raspberry Pi OS.

## Setup

### Telegram Bot
1. Create a Telegram bot: https://core.telegram.org/bots#how-do-i-create-a-bot
2. Send a message to the bot to create a Chat ID.
3. configure in config.yml the TELEGRAM_API_KEY.

### Refresh Bot
1. Run the follow install commands
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
playwright install
python3 main.py [path to config.yml]
```

2. Install VNC, optionally, for remote access
```
sudo raspi-config
# Select Interfacing Options > VNC > Yes
```