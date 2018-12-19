import socket
import SerialPortCommunication
from threading import Thread
from time import sleep
import time
from datetime import datetime, timedelta
import sys, os
import re

# 1-listen to 5060 for receiving data from phone
# 2-listen to 9090 for receiving data from asterisk
# 3-send all the data which you received from phone to asterisk server to port 6060 from the socket 9090
# 4-send all the data which you received from asterisk to phone
# 5-add listener functionally to asterisk socket and phone Socket
# 6-create a serial port communication which has ability to send and receive data async
# 7-create a protocol to call, answer, hangup

voiceData =       b'00000000000000000000'
lastAsteriskRTP = b'00000000000000000000000000000000'
lastTelephoeRTP = b'00000000000000000000000000000000'

asteriskRTPPort = 10000
telephoneRTPPort = 5004

isAnswered = False
CallIncome = False
# isAnsweredReceived=False

RTPBegingData =    '\x21\x6B\x50\x00'
RingBeginData =    '\x21\x6B\x50\x01\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA'
HangupBeginData =  '\x21\x6B\x50\x02\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA'
AnswerBegingData = '\x21\x6B\x50\x03\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA'

# listen to all ip from port 5060
def BindTelephone(UDP_IP_ADDRESS='0.0.0.0', UDP_PORT_NO=5060):
    print('BindTelephone is running...')
    telephoneSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    while True:
        # get 10000 byte from 5060
        data, addr = telephoneSock.recvfrom(10000)
        # replace phone ip and port with computer
        data = data.replace('192.168.0.100:8080', '192.168.0.102:9090')
        # replace some string data
        data = data.replace('192.168.0.100', '192.168.0.102')
        data = data.replace('invalid:5060', 'invalid:6060')
        data = data.replace('192.168.0.102:5060', '192.168.0.102:6060')

        if "REGISTER sip" in data:
            print("RegisterSIP has been sent.")

        if 'm=audio' in data:
            print('Telephone RTP Settings is Changing.')
            indexofM_Audio = data.find('m=audio')
            index_of_RTP = data.find('RTP', indexofM_Audio)
            replacementData = data[indexofM_Audio:index_of_RTP]
            global telephoneRTPPort
            telephoneRTPPort = int(data[indexofM_Audio+len('m=audio'): index_of_RTP])
            print('Telephone RTP Port is: ' + str(telephoneRTPPort))
            data = data.replace(replacementData, 'm=audio 20000 ')

        print('Sending SIP Packet To Asterisk Engine.')
        asteriskSock.sendto(data, ('192.168.0.102', 6060))

        if 'INVITE sip:100' in data:
            now = datetime.now().time().strftime('%H:%M:%S')
            global lastCallTime

            if (datetime.strptime(now,'%H:%M:%S') - datetime.strptime(lastCallTime,'%H:%M:%S')) >= timedelta(seconds=3):
                global isAnswered
                isAnswered = False
                lastCallTime = datetime.now().time().strftime('%H:%M:%S')
                print('RingPacket has been sent.')

                if not isAnswered:
                    for i in range(6):
                        SerialPortCommunication.sendData(RingBeginData)
                        sleep(0.01)

        elif "BYE sip:" in data:
            print('HangupPacket has been sent.')
            global isAnswered
            isAnswered = False

            for i in range(6):
                SerialPortCommunication.sendData(HangupBeginData)
                sleep(0.01)

        elif "SIP/2.0 200 OK" in data and "Via: SIP/2.0/UDP 192.168.0.102:5060":
            global isAnswered
            isAnswered=True
            print("Phone has been answered.")

            for i in range(6):
                SerialPortCommunication.sendData(AnswerBegingData)
                print("AnswerBegingData has been sent.")
                sleep(0.01)

def BindAsterisk(UDP_IP_ADDRESS='0.0.0.0', UDP_PORT_NO=9090):
    print('BindAsterisk is running...')
    asteriskSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    while True:
        data, addr = asteriskSock.recvfrom(10000)
        data = data.replace('192.168.0.102:6060', '192.168.0.102:5060')
        data = data.replace('invalid:6060', 'invalid:5060')
        data = data.replace('192.168.0.102:9090', '192.168.0.100:8080')
        data = data.replace('rport=9090', 'rport=5060')
        data = data.replace('192.168.0.102:6060', '192.168.0.102:5060')

        if 'm=audio' in data:
            # print('Changing Asterisk RTP Settings')
            indexofM_Audio = data.find('m=audio')
            index_of_RTP = data.find('RTP', indexofM_Audio)
            replacementData = data[indexofM_Audio:index_of_RTP]
            global asteriskRTPPort
            asteriskRTPPort = int(data[indexofM_Audio+len('m=audio'): index_of_RTP])
            print('asteriskRTPPort is: ' + str(asteriskRTPPort) )
            data = data.replace(replacementData, 'm=audio 19000 ')

        telephoneSock.sendto(data, ('192.168.0.100', 8080))
        print('SIPPacket has been sent.')


def BindTelephoneRTP(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=19000):
    print('BindTelephoneRTP is running...')
    telephoneRTPSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    while True:
        data, addr = telephoneRTPSock.recvfrom(500)
        mydata = data
        newdata = data[-20:]
        newdata = RTPBegingData + newdata
        asteriskRTPSock.sendto(data, ('192.168.0.102', asteriskRTPPort))

        global isAnswered
        if isAnswered:
            SerialPortCommunication.sendData(newdata)
            # with open("SSEND", "ab") as file_send:
            #     file_send.write(newdata)

def BindAsteriskRTP(UDP_IP_ADDRESS='192.168.0.102', UDP_PORT_NO=20000):
    print('BindAsteriskRTP is running...')
    asteriskRTPSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

    while True:
        data, addr = asteriskRTPSock.recvfrom(500)
        global lastAsteriskRTP
        global voiceData
        global isAnswered
        lastAsteriskRTP = data
        mydata = data

        if isAnswered == True:
            mydata = data[:12] + voiceData

        if len(data) != 32:
            mydata += '\xAA'*(32-len(data) )
        else:
            telephoneRTPSock.sendto(mydata, ('192.168.0.100', telephoneRTPPort))
            telephoneRTPSock.sendto(lastAsteriskRTP, ('192.168.0.100', telephoneRTPPort))


def dataReceivedFromSerial(data):
     print('dataReceivedFromSerial is running...')

     if RingBeginData in data:
        global CallIncome
        print ('RingBeginPacket received.')
        global isAnswered
        isAnswered = False
        os.system('''sudo asterisk -rvvvx "console dial 200" ''')

     elif HangupBeginData in data:
         print ('HangupPacket Received')
         os.system('''sudo asterisk -rvvvx "hangup request all" ''')
         global isAnswered
         isAnswered = False

     elif RTPBegingData in data:
        print ('SerialPort RTPPacket Received.')
        global voiceData
        data = data[4:]
        voiceData = data

     elif AnswerBegingData in data:
         print("AnswerBegingData has been received")
         global isAnswered
         isAnswered = True

     else:
         print("Unknown Data Type!")
         print("Unknown Data Content Is: ", data)

if __name__ == '__main__':

     global lastCallTime
     lastCallTime = datetime.now().time().strftime('%H:%M:%S')

     telephoneSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     asteriskSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     telephoneRTPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     asteriskRTPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

     threadAsterisk = Thread(target = BindAsterisk)
     threadPhone = Thread(target = BindTelephone)
     threadRTPAsterisk = Thread(target = BindAsteriskRTP)
     threadRTPPhone = Thread(target = BindTelephoneRTP)

     threadAsterisk.start()
     threadPhone.start()
     threadRTPAsterisk.start()
     threadRTPPhone.start()

     SerialPortCommunication.onReceivedData(dataReceivedFromSerial)
     SerialPortCommunication.init("/dev/ttyUSB0", 38400)

     print ('Serial Port is Open')

     threadAsterisk.join()
     threadPhone.join()
     threadRTPAsterisk.join()
     threadRTPPhone.join()
