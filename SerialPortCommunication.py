import serial
from threading import Thread
from functools import wraps

ser = serial.Serial()
global event


def sendData(data):
    if ser.is_open:
        ser.write(data)


def startReceiving():
    while True:
        if ser.is_open:
            s = ser.read(20)
            global event
            event(s)


def onReceivedData(func):
    global event
    event = func


def init(portName, baudRate):
    ser.baudrate = baudRate
    ser.port = portName
    ser.open()
    if ser.is_open:
        receivingThread = Thread(target=startReceiving)
        receivingThread.start()
