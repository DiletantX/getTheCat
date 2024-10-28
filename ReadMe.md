# GetTheCat

Do you want cats out of your garden automatically with AI and notification to your mobile (with photo of the intruder)? Then continue reading!

## Introduction
For those who have a garden or any piece of land, cats making toilet there is a known problem. 
This problem has a lot of solutions which don't work, including the ones which I checked myself: 
- various smells (coffee, lavanda flowers, vinegar)

As well as ones which I didn't check myself, suh as:
- devices with ultrasound activated by motion sensor

There are also exotic solutions, such a smell of urina of big predators (wolfs, tigers), which can be found in internet as well. I believe the reader of this can guess why the last one isn't a good option :).

The only way to solve the "cat's excrements" problem is to make a proper solution. It should be effective enough,
being at the same time ethical.

## System Design

### Concept
The main idea is to detect cats on video from surveillance camera, using a technology which can 
recognize cats from humans and other animals. When the recognition is made, the monitoring part of the 
system should inform the owner, and the active part of the system should ensure cat is gone. The latter
is the most challenging since we need an ethical way of doing it. Fire-gun or catapult are not ethical enough.
Eventually the decision is made for a water sprinkler.

I must mention that cats have quite high organized intellect. Cats can learn and adapt to new conditions.
This fact actually makes the solutions listed in the introduction (like smells or ultrasound) not effective:
a cat can be afraid of ultrasound or a new smell introduced first time, though second time or third time 
the cat will understand that this doesn't make any harm. That's why the solution with a water sprinkler is 
one of the obvious: cats dislike to be wet, so they can't adapt to it; and this solution is ethical
as well because it doesn't bring any risk to cat's health. It's the same as a rain: cats can be outside during rain,
though they would likely prefer to be under roof.

### Implementation

The system shall include hardware and hydro/mechanical parts as follows:
1. Video Camera with good resolution and infrared light to enable night vision. It shall be for outdoor use. IMPORTANT: the camera shall only monitor your properties, so adjust the position accordingly. In many countries it is illegal to monitor someone else's properties. The camera shall have network connectivity. Camera shall be installed no lower than 1.5-2 m from ground.  Ideally use one camera for area around 3x3 to 5x5 meters (may also work on bigger territory if resolution is enough, but wasn't tested).
2. Server for video processing. Most of old laptops (which normally exist in all families) will serve well. Example: tested on ASUS K73SV bought in 2011, CPU Intel(R) Core(TM) i3-2310M CPU @ 2.10GHz 2 cores, RAM 4 GB. Ideally the laptop shall be able to run Debian (tested on Debian Trixie). Server should have USB and network connectivity.
3. Water sprinkler installed on ground in the middle of the monitored zone. Sprinkler sohuld sprinkle water to all directions 360 degrees around, which is true for rotating sprinkler. However, you may need other types of sprinklers depending on configuration of the specific monitoring area. 
4. Water hose from normal tap pressure point to the sprinkler. No specific requirements, just ensure the lengh is enough and that you have necessary fitting if needed (i.e. 1/2 inch to 3/4 inch). 
5. Water valve (12 V normally closed solenoid valve) installed in the hose before the sprinkler to control water. You can try other types, but I recommend to use as low as possible supply voltage.
6. DC supply block 12 V (or whatever is compatible with the valve). 
7. Electrical relay connected by USB to the server to control DC supply of the water valve. 
8. All necessary wiring: ethernet cable between camera and the server, supply cable of the camera, supply cable of the valve (controlled by electrical switch)

The getTheCat software is running continuously on the server and monitors video frames. In case a cat is detected, the system activates electric relay and sends telegram notification. Also it saves 10 seconds of video in the folder 'video'. In case there are humans detected, the system blocks itself for several seconds.  
The software used the library imageAI (Copyright (c) 2019 MOSES OLAFENWA), and modules to handle video, electrical relay and telegram notifications.

### Hardware Example Links

Following links are just examples, you may use other hardware as long as it complies with requirements above.

* [Camera](https://www.aliexpress.com/item/1005005048005737.html?spm=a2g0n.order_detail.order_detail_item.2.49b5f19cTuyzWb&_gl=1*1evxxek*_gcl_aw*R0NMLjE3Mjg4OTA1MzQuQ2owS0NRandnck80QmhDMkFSSXNBS1E3elVrdk9CQzJWQmxHYjc3VVhKRW5MOTZEZzZ5NlBfU3pxSnI5MURKcHNmcW1mbWhoQXFZMkQyWWFBaU53RUFMd193Y0I.*_gcl_au*MTYxNDkwNTMzNy4xNzIyNTE1MTgz*_ga*MTg1MDYyODUzMi4xNzIyNTE1MTgy*_ga_VED1YSGNC7*MTcyODg5MDUwNC4xNS4xLjE3Mjg4OTA1NjEuMy4wLjA)

![Camera](./doc/camera.png)

* [Valve](https://www.aliexpress.com/item/1005005253916656.html?spm=a2g0n.order_detail.order_detail_item.2.1457f19caV9FbF&_gl=1*lnc669*_gcl_aw*R0NMLjE3Mjg4OTA1MzQuQ2owS0NRandnck80QmhDMkFSSXNBS1E3elVrdk9CQzJWQmxHYjc3VVhKRW5MOTZEZzZ5NlBfU3pxSnI5MURKcHNmcW1mbWhoQXFZMkQyWWFBaU53RUFMd193Y0I.*_gcl_au*MTYxNDkwNTMzNy4xNzIyNTE1MTgz*_ga*MTg1MDYyODUzMi4xNzIyNTE1MTgy*_ga_VED1YSGNC7*MTcyODg5MDUwNC4xNS4xLjE3Mjg4OTA3MzEuNDUuMC4w)

![Valve](./doc/valve.png)

* [Relay USB](https://www.aliexpress.com/item/1005005654268525.html?spm=a2g0n.order_detail.order_detail_item.2.f323f19cmq5Z02&_gl=1*1c1wijg*_gcl_aw*R0NMLjE3Mjg4OTA1MzQuQ2owS0NRandnck80QmhDMkFSSXNBS1E3elVrdk9CQzJWQmxHYjc3VVhKRW5MOTZEZzZ5NlBfU3pxSnI5MURKcHNmcW1mbWhoQXFZMkQyWWFBaU53RUFMd193Y0I.*_gcl_au*MTYxNDkwNTMzNy4xNzIyNTE1MTgz*_ga*MTg1MDYyODUzMi4xNzIyNTE1MTgy*_ga_VED1YSGNC7*MTcyODg5MDUwNC4xNS4xLjE3Mjg4OTA5NjYuNTEuMC4w)

![Relay USB](./doc/relay.png)

* [Sprinkler](https://www.aliexpress.com/item/4000124520501.html?spm=a2g0n.order_detail.order_detail_item.2.6075f19cVETGgQ&_gl=1*7d9gif*_gcl_aw*R0NMLjE3Mjg4OTEwNjguQ2owS0NRandnck80QmhDMkFSSXNBS1E3elVrdk9CQzJWQmxHYjc3VVhKRW5MOTZEZzZ5NlBfU3pxSnI5MURKcHNmcW1mbWhoQXFZMkQyWWFBaU53RUFMd193Y0I.*_gcl_au*MTYxNDkwNTMzNy4xNzIyNTE1MTgz*_ga*MTg1MDYyODUzMi4xNzIyNTE1MTgy*_ga_VED1YSGNC7*MTcyODg5MDUwNC4xNS4xLjE3Mjg4OTEwNzUuMzAuMC4w)

![Sprinkler](./doc/sprinkler.png)

## Software Installation

### Operating System for Server
Software is in python3, so it will theoretically work in any OS which supports python3. Tested on Debian Pixie and Windows 10.

[Installation of debian](https://d-i.debian.org/doc/installation-guide/en.amd64/index.html)
Alternatively, you can try to use existing OS on your old laptop (Windows or Mac OS), though I would recommend to anyway upgrade (or re-install) to the latest version of your preferred OS. If your laptop is 5-10 years old, the OS version there can be too old.

### GetTheCat software

#### Clone this repository

    git clone https://github.com/DiletantX/getTheCat

#### Download the YOLOv3 model

[Download YOLOv3](https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt)

The file .pt should be at the same level as getTheCat directory.

#### Install dependencies for imageAI (CPU):

    cd getTheCat
    pip install -r requirements.txt

Alternatively, install dependencies GPU (advanced way, for using GPU you should have compatible drivers:

    pip install -r requirements_gpu.txt

The project uses [imageAI library](https://github.com/OlafenwaMoses/ImageAI)

#### Install other dependencies:
Tkinter is installed by apt on Debian: (but on Windows it is installed by pip as I remember)

    # On Debian:
    sudo apt install python3-tk

Install image ai (if not yet installed)

    pip install imageai

#### Set up telegram notifications and add secret.py

Create a free-of-charge bot in Telegram using [this manual](https://core.telegram.org/bots/tutorial).

As soon as you have bot_token, you can manually send message to your bot channel and then execute the commented out function get_channel_id() from the telegram_notification to get your channel_id.

Create the file secret.py and define bot_token and channel_id there. 

To test telegram notifications run:

    python telegram_notification.py

Expected results: no exceptions, valid response, you got a test message in your bot's channel.

In case you don't need telegram notifications - remove it from the ReadFramesAndWorkWithLastFrame.py.

#### Test installation

Telegram notifications are covered by this test. If you don't need them - remove from code.
In this manual we don't describe how to use virtual environment for python. This information is easy to find.

Activate the python virtual environment and test installation:

    cd getTheCat
    python selected_detections_test.py

Expected result (console output):

    ...
    detected white = True
    ...

Expected: Telegram notification is sent.

#### Set up camera URL

Connect camera to supply and network, Ensure you can ping it and connect with browser to set configure. 

Set up your camera to be reachable in the network. Set up the best resolution. Most surveilance cameras have 2 streams: main and secondary, we should normally aim for the main stream since it usually has better resolution. URL differs for main and secondary streams. 
The protocols can be RTSP or HTTP, which also impacts URL.

In the ReadFramesAndWorkWithLastFrame.py define URL, for example for the camera mentioned in the hardware examples:

    stream_url = 'rtsp://admin:123456@192.168.1.10:554/stream1'

Note, that if you have an expensive camera, configuration is described in the manual. Though for many cameras from aliezpress or cheap shops this is not the case. Don't worry: usually this is quite easy to find or guess the URR for main stream. Ask ChatGPT or search for info for most used default URLs.

#### Set up USB relay
In case you used the same USB relay model as referenced in hardware examples, you need to define USB relay path in the file usb_relay.py.

On Windows insert USB relay and check port in Device Manager. Example port:

    PORT = 'COM3'

On Linux insert USB relay and check device path by command ls /dev/ttyUSB*. Example port:

    PORT = '/dev/ttyUSB0'

For test run:

    python usb_relay.py

If the port is defined correctly, the LED on he USB relay should be ON for 10 seconds. 

### Software Usage

    python3 ReadFramesAndWorkWithLastFrame.py

Enjoy!

### Validate the system operation

You can use a picture of the cat to validate the system work. Ensure that there are no humans in camera view and demonstrate a picture of a cat from distance ~ 0.5 - 1 m. Expected result: after several seconds the system will send telegram notification and activate the water sprinkler.
You can of course test it with real physical cat if you have volunteering one (just ensure he signed NDA). 

## Cats Pictures

Everything is better with cats images. So enjoy 2 detections:

* Night Cat
![catnight](./doc/cat_night.jpg)
* Day Cat
![catday](./doc/cat_day.jpg)