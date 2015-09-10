#!/usr/bin/env python

# CSC 895: DO IT YOURSELF BURGLAR ALARM, Fall 2015
# Arno Puder, Pratik Jaiswal
# Python server that is responsible for sending notifications on Android phone.
# Byte reception of 1 indicates that motion is deteceted by the sensor and this 
# will trigger script to send user-defined message to the Android phone. 
# Libraries:
#    1. serial - allows python to read serial data
#    2. requests - allows python to make REST API requests (here - Twilio)

import serial
import requests
from datetime import datetime, timedelta
from twilio.rest import TwilioRestClient

# Set the serial port by taking a look at Arduino IDE configurations (Tools > Serial Port")
# For an instance, SERIAL_PORT = "/dev/tty.usbserial-A70064Mh"

SERIAL_PORT = "/dev/tty.usbmodem621"
SERIAL_BAUD = 115200

# Restrict to a single notification every 15 minutes
SENSOR_INTERVAL = timedelta(minutes=15)

# Registered number on twilio.com
SMS_FROM = "+14159368740"

# Your cell phone number
SMS_TO = "+14153073703"

# You can find account_sid and account_token on twilio dashboard
# https://www.twilio.com/user/account/voice-sms-mms/getting-started
TWILIO_ACCOUNT_SID = "ACc5a978555d7ba8899761661b2d1e4c46"
TWILIO_TOKEN = "604c445eee2ecae2a9e1cb63c2a6b9be"

# Optional: You can save SID and TOKEN in a local file and import it (here - settings.py file)
try:
    from settings import *
except ImportError:
    pass	

# Twilio URL - python will make use of it to make rest API call by accessing your account
TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/ACc5a978555d7ba8899761661b2d1e4c46/SMS/Messages"

# Start the server
if __name__ == "__main__":
    print "Starting Motion Detector Server at", datetime.now()
    last_sent_time = None

    # Open a serial connection to the Arduino
    with serial.Serial(SERIAL_PORT, SERIAL_BAUD) as arduino:
        while True:
            print "Pinging Arduino..."

            # Listen to the Arduino and look for a byte
            byte_received = arduino.read()
            print "Received byte:", byte_received

            # Alert! Motion is detected
            if byte_received == "1":
                print "Motion Detected at", datetime.now()

                # Send a notification if you have not in the last 15 minutes
                if not last_sent_time or (datetime.now() - last_sent_time) > SENSOR_INTERVAL:
                    last_sent_time = datetime.now()
                    print "Sending notification..."

                    # Send request to Twilio to send notification
                    try:
                        client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_TOKEN)
                        message = client.messages.create(body="Pratik, something is fishy at home!",
                                to=SMS_TO, from_=SMS_FROM)
                        print message.sid
                        print "** Notification Sent! **"

                    except Exception as e:
                        print "Some error occurred while sending notification:", e