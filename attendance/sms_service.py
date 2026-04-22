import serial
import time

class SMSService:
    def __init__(self, port='COM3', baudrate=9600):
        self.port = serial.Serial(port, baudrate, timeout=10)
        time.sleep(2)

    def send_sms(self, phone, message):
        self.port.write(b'AT\r')
        time.sleep(1)

        self.port.write(b'AT+CMGF=1\r')
        time.sleep(1)

        cmd = f'AT+CMGS="{phone}"\r'
        self.port.write(cmd.ecode())
        time.sleep(1)

        self.port.write(message.encode())
        self.port.write(bytes([26]))

        time.sleep(3)
        print(f"SMS sent to {phone}")


