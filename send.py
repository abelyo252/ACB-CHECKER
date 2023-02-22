"""
Python to Arduino Serial Communication
By: Abel Yohannes
Internship Project for jimma university
"""


import serial
import time

arduino = serial.Serial('COM2', 9600)
time.sleep(2)

print("ACB Try to Communicate With Arduino")


def sendAngle(a1=0,a2=0,a3=0,a4=0):
    sent_message = str(a1)+","+str(a2)+","+str(a3)+","+str(a4)
    arduino.write(bytes(sent_message, 'ascii'))
    print("Message Sent!")

sendAngle(10,20,30,40)

