import serial

import time



usb_relay = serial.Serial("COM3",9600)


if usb_relay.is_open:

   print(usb_relay)

   on_cmd = b'\xA0\x01\x01\xA2'

   off_cmd =  b'\xA0\x01\x00\xA1'

   usb_relay.write(on_cmd )

   time.sleep(2)

   usb_relay.write(off_cmd)

   time.sleep(2)


usb_relay.close()