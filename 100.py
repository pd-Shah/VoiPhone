import socket, sys
import SerialPortCommunication
from threading import Thread
from time import sleep
from struct import *
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


# def check_rtp_or_sip(packet):
#     udph_length = 8
#     udp_header = packet[:8]
#
#     #now unpack them :)
#     udph = unpack('!HHHH' , udp_header)
#     source_port = udph[0]
#     dest_port = udph[1]
#     length = udph[2]
#     checksum = udph[3]
#
#     # print 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(length) + ' Checksum : ' + str(checksum)
#
#     h_size = eth_length + iph_length + udph_length
#     data_size = len(packet) - h_size
#
#     #get data from the packet
#     data = packet[h_size:]
#
#
#     # SIP
#     if source_port==5060 and dest_port==5060:
#         print"packet is SIP"
#         print(data)
#     # RTP
#     else:
#         print "packet is RTP"
#         # print("header:"+ data[:12])
#         # print("payloaddata:" + data[12:])
#
#         counter+=1
#         print counter
#         if counter >=1000:
#             output_file.write(myfile)
#             output_file.close()
#             print 'file is closed'
#         else:
#             myfile+=data[:]
#             # print "*"*10
#             # print type(data)
#             # print type(myfile)
#             # print "*"*10
#             print 'file not closed'
#             # output_file.write(data[12:])
#
#     print  'Size header: ' + str(h_size) + 'Data : ' + data + "udph:" + str(udph) + "u length: "  + str(u) + "data_size:"+  str(data_size)
#



def BindTelephone(UDP_IP_ADDRESS='0.0.0.0', UDP_PORT_NO=5060):
    telephoneSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        print('BindTelephone')
        data, addr = telephoneSock.recvfrom(10000)
        print ("Recive: ", data)
        # if the data is about registeration send it to asterisk
        # check_rtp_or_sip()
        asteriskSock.sendto(data, ('127.0.0.1', 6060))
        # otherwise send abbreviation of ringing and rtp and hangup from serial
        # SerialPortCommunication.sendData("ringing")
        # SerialPortCommunication.sendData("hangup")
        # SerialPortCommunication.sendData(rtp)

        print ("Send: ", data)

def BindAsterisk(UDP_IP_ADDRESS='0.0.0.0', UDP_PORT_NO=9090):
    asteriskSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
    while True:
        print('BindAsterisk')
        data, addr = asteriskSock.recvfrom(10000)
        print ("Recive: ", data)
        telephoneSock.sendto(data, ('192.168.0.101', 5060))

        print ("Send: ", data)

# def dataReceivedFromSerial(data):
#     #ringing
#
#     #hangup
#     #20 byte rtp
#         SerialPortCommunication.sendData("salam")



if __name__ == '__main__':
    telephoneSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    asteriskSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    threadAsterisk = Thread(target = BindAsterisk)
    threadPhone = Thread(target = BindTelephone)
    threadAsterisk.start()
    threadPhone.start()
    threadAsterisk.join()
    threadPhone.join()
    # SerialPortCommunication.onReceivedData(dataReceivedFromSerial)
    # SerialPortCommunication.init("/dev/ttyUSB0", 115200)
