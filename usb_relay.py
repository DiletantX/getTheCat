import serial
import time


def relay_on_for_x_sec(x: int):

    usb_relay_com_port = serial.Serial("COM3",9600)

    if usb_relay_com_port.is_open:

       print(usb_relay_com_port)

       on_cmd = b'\xA0\x01\x01\xA2'

       off_cmd =  b'\xA0\x01\x00\xA1'

       usb_relay_com_port.write(on_cmd )

       time.sleep(10)

       usb_relay_com_port.write(off_cmd)


    usb_relay_com_port.close()


if __name__ == '__main__':
    relay_on_for_x_sec(10)
