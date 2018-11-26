import socket
import SerialPortCommunication
from threading import Thread
from time import sleep
#
# def client(message ,UDP_IP_ADDRESS, UDP_PORT_NO):
#     clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))

# 1-listen to 5060 for receiving data from phone
# 2-listen to 9090 for receiving data from asterisk
# 3-send all the data which you received from phone to asterisk server to port 6060 from the socket 9090
# 4-send all the data which you received from asterisk to phone
# 5-add listener functionally to asterisk socket and phone Socket
# 6-create a serial port communication which has ability to send and receive data async
# 7-create a protocol to call, answer, hangup



def BindTelephone(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=5060):
    telephoneSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        data, addr = telephoneSock.recvfrom(10000)
        print ("Recive: ", data)

        asteriskSock.sendto(data, ('127.0.0.1', 6060))
        print ("Send: ", data)

def BindAsterisk(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=9090):
    asteriskSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        data, addr = asteriskSock.recvfrom(10000)
        print ("Recive: ", data)

        telephoneSock.sendto(data, ('192.168.0.101', 5060))
        print ("Send: ", data)

def dataReceivedFromSerial(data)
     print data

if __name__ == '__main__':
    # telephoneSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # asteriskSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # threadAsterisk = Thread(target = BindAsterisk)
    # threadPhone = Thread(target = BindTelephone)
    # threadAsterisk.start()
    # threadPhone.start()
    # threadAsterisk.join()
    # threadPhone.join()
    SerialPortCommunication.onReceivedData(dataReceivedFromSerial)
    SerialPortCommunication.init("/dev/ttyUSB0", 115200)
    while True:
        SerialPortCommunication.sendData("salam")
