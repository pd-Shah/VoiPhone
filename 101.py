import socket
import SerialPortCommunication
from threading import Thread
from time import sleep
from packetize import RtpPacket
import os
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
packetize = RtpPacket()
palloadData = b'00000000000000000000'

def BindTelephone(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=5060):
    telephoneSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        data, addr = telephoneSock.recvfrom(10000)
        # data = data.replace('192.168.0.101:8080', '127.0.0.1:9090')
        # data = data.replace('192.168.0.101', '127.0.0.1')

        # print(len(data))
        # if 'INVITE' in data:
            # SerialPortCommunication.sendData("ring")
        # elif "BYE" in data:
            # SerialPortCommunication.sendData("hangup")
        # else:
        asteriskSock.sendto(data, ('127.0.0.1', 6060))


def BindAsterisk(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=9090):
    asteriskSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        data, addr = asteriskSock.recvfrom(10000)
        # data = data.replace('127.0.0.1:6060', '192.168.0.102:5060')
        # data = data.replace('127.0.0.1:9090', '192.168.0.102:5060')
        # data = data.replace('127.0.0.1', '192.168.0.101')
        # data = data.replace('rport=9090', 'rport=5060')
        # data = data.replace('192.168.0.102:6060', '192.168.0.102:5060')

        print ("Receive Data asteriskSock")
        if len(data) == 74:
            print('Start Packetizing')
            packetize.make_header(payload=palloadData)
            p = packetize.getPacket()
            telephoneSock.sendto(p, ('192.168.0.101', 8080))
        else:
            telephoneSock.sendto(data, ('192.168.0.101', 8080))
        print ("Send: Data telephoneSock")


def dataReceivedFromSerial(data):
    print (data)

    if "ring" in data:
        os.system('''sudo asterisk -rvvvx "originate SIP/192.168.0.101 extension" ''')
    elif "hangup" in data:
        os.system('''sudo asterisk -rvvvx "hangup request all" ''')
    else:
        palloadData = data





if __name__ == '__main__':
     telephoneSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     asteriskSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     threadAsterisk = Thread(target = BindAsterisk)
     threadPhone = Thread(target = BindTelephone)
     threadAsterisk.start()
     threadPhone.start()
     SerialPortCommunication.onReceivedData(dataReceivedFromSerial)
     SerialPortCommunication.init("/dev/ttyUSB0", 115200)
     threadAsterisk.join()
     threadPhone.join()
#    while True:
#        SerialPortCommunication.sendData("salam")
