import SerialPortCommunication
from threading import Thread

def dataReceivedFromSerial(data):
     print (data)

if __name__ == '__main__':
      SerialPortCommunication.onReceivedData(dataReceivedFromSerial)
      SerialPortCommunication.init("/dev/ttyUSB1", 115200)
