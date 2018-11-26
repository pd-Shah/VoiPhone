import socket
import SerialPortCommunication
from threading import Thread
from time import sleep
from packetize import RtpPacket
import sys, os
import re

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
voiceData = b'00000000000000000000'
lastAsteriskRTP = b'00000000000000000000000000000000'
lastTelephoeRTP = b'00000000000000000000000000000000'

asteriskRTPPort = 10000
telephoneRTPPort = 5004

def BindTelephone(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=5060):
    telephoneSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        data, addr = telephoneSock.recvfrom(10000)
        data = data.replace('192.168.0.100:8080', '127.0.0.1:9090')
        data = data.replace('192.168.0.100', '127.0.0.1')
        if 'INVITE sip:100' in data:
            print('ringging...')
            SerialPortCommunication.sendData("ring")
        elif "BYE sip:" in data:
            print('finishing...')
            SerialPortCommunication.sendData("hangup")
        if 'm=audio' in data:
            indexofM_Audio = data.find('m=audio')
            index_of_RTP = data.find('RTP', indexofM_Audio)
            replacementData = data[indexofM_Audio:index_of_RTP]
            global telephoneRTPPort
            telephoneRTPPort = int(data[indexofM_Audio+len('m audio'): index_of_RTP])
            print('Telephone RTP Port is'+str(telephoneRTPPort))
            data = data.replace(replacementData, 'm=audio 20000 ')
        asteriskSock.sendto(data, ('127.0.0.1', 6060))


def BindAsterisk(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=9090):
    asteriskSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        data, addr = asteriskSock.recvfrom(10000)
        data = data.replace('127.0.0.1:6060', '192.168.0.102:5060')
        data = data.replace('127.0.0.1:9090', '192.168.0.102:5060')
        data = data.replace('127.0.0.1', '192.168.0.100')
        data = data.replace('rport=9090', 'rport=5060')
        data = data.replace('192.168.0.102:6060', '192.168.0.102:5060')
        if 'm=audio' in data:
            print('exist')
            indexofM_Audio = data.find('m=audio')
            index_of_RTP = data.find('RTP', indexofM_Audio)
            replacementData = data[indexofM_Audio:index_of_RTP]
            global asteriskRTPPort
            asteriskRTPPort = int(data[indexofM_Audio+len('m audio'): index_of_RTP])
            print('Asterisk RTP Port is' + str(telephoneRTPPort))
            data = data.replace(replacementData, 'm=audio 19000 ')
        else:
            print('does not exist')
        telephoneSock.sendto(data, ('192.168.0.100', 8080))


#
def BindTelephoneRTP(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=19000):
    telephoneRTPSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        data, addr = telephoneRTPSock.recvfrom(500)
        mydata = data
        newdata = data[-20:]
        SerialPortCommunication.sendData(newdata)
        asteriskRTPSock.sendto(data, ('192.168.0.102', asteriskRTPPort))
        # global lastAsteriskRTP
        # mydata = lastAsteriskRTP[:12] + voiceData
        # telephoneRTPSock.sendto(mydata, ('192.168.0.101', telephoneRTPPort))

def BindAsteriskRTP(UDP_IP_ADDRESS='127.0.0.1', UDP_PORT_NO=20000):
    asteriskRTPSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        print 'start to receiving data from asterisk server'
        data, addr = asteriskRTPSock.recvfrom(500)
        print('asterisk rtp data received')
        global lastAsteriskRTP
        lastAsteriskRTP = data
        mydata = lastAsteriskRTP[:12] + voiceData
        telephoneRTPSock.sendto(mydata, ('192.168.0.100', telephoneRTPPort))
        # lastAsteriskRTP = data.replace(data[-20:], voiceData)

        print 'data is changed and ready to send to phone'
        # telephoneRTPSock.sendto(data, ('192.168.0.101', telephoneRTPPort))



def dataReceivedFromSerial(data):
    # if "ring" in data:
    #     # os.system('''sudo asterisk -rvvvx "originate SIP/192.168.0.101 extension" ''')
    # elif "hangup" in data:
    #     os.system('''sudo asterisk -rvvvx "hangup request all" ''')
    # else:
    if "ring" in data:
         os.system("sudo asterisk -rx 'console dial 100'")
    else:
        global voiceData
        voiceData = data
        print (len(data))



if __name__ == '__main__':

     os.system("sudo asterisk -rx 'console dial 100'")
    # initializing socket for rtp and sip
     telephoneSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     asteriskSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     telephoneRTPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     asteriskRTPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # createing async input and output
     threadAsterisk = Thread(target = BindAsterisk)
     threadPhone = Thread(target = BindTelephone)
     threadRTPAsterisk = Thread(target = BindAsteriskRTP)
     threadRTPPhone = Thread(target = BindTelephoneRTP)

     threadAsterisk.start()
     threadPhone.start()
     threadRTPAsterisk.start()
     threadRTPPhone.start()

     SerialPortCommunication.onReceivedData(dataReceivedFromSerial)
     SerialPortCommunication.init("/dev/ttyUSB0", 115200)
     threadAsterisk.join()
     threadPhone.join()
     threadRTPAsterisk.join()
     threadRTPPhone.join()
#    while True:
#        SerialPortCommunication.sendData("salam")
