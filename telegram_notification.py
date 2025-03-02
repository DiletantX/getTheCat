import requests
from secret import *
import threading
import traceback
from logger import get_logger


# Sending Telegram message can sometimes take a second or a few, so it
# is put to a thread to avoid delays in the main execution

def send_telegram_message_th(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': channel_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()


def send_telegram_image_th(image_path, caption=""):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    data = {'chat_id': channel_id, 'caption': caption}
    resp = requests.Response()
    resp.status_code = 500  # Indicate failure by default
    resp._content = b'{"error": "no response"}'

    try:
        with open(image_path, 'rb') as file:
            files = {'photo': file}
            resp = requests.post(url, files=files, data=data)
    except:
        error_message = traceback.format_exc()
        get_logger().error("ERROR in sending telegram notification:")
        get_logger().error(error_message)
    finally:
        get_logger().debug("Sending telegram notification complete")
        return resp.json()


def send_telegram_message(message):
    thread1 = threading.Thread(target=send_telegram_message_th(message))


def send_telegram_image(image_path, caption=""):
    get_logger().debug("Sending telegram notification started")
    thread1 = threading.Thread(target=send_telegram_image_th(image_path, caption))


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


# Send a test message manually for Telegram app to your channel before running this
#channel_id = get_channel_id()
#print(f"Channel ID: {channel_id}")

if __name__ == '__main__':
    response = send_telegram_message("Hello, this is a test message from my Python app!")
    print(response)

# Test sending the image
#response = send_telegram_image("last.jpg", "Here is an image from my bot")
#print(response)
