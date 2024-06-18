import requests
from secret import *


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': channel_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


def send_telegram_image(image_path, caption=""):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': channel_id, 'caption': caption}

    response = requests.post(url, files=files, data=data)
    return response.json()


def get_channel_id():
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url)
    updates = response.json()

    # Print updates to inspect the structure
    print(updates)

    if updates['ok']:
        for update in updates['result']:
            if 'channel_post' in update:
                channel_id = update['channel_post']['chat']['id']
                return channel_id
    return None


# Send a test message to your channel before running this
#channel_id = get_channel_id()
#print(f"Channel ID: {channel_id}")


# Test the function
#response = send_telegram_message("Hello, this is a test message from my Python app!")
#print(response)

# Test sending the image
#response = send_telegram_image("last.jpg", "Here is an image from my bot")
#print(response)
