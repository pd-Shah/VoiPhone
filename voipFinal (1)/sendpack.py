import socket
# addressing information of target
IPADDR = '192.168.0.101'
PORTNUM = 5004
# enter the data content of the UDP packet as hex
PACKETDATA = 'f1a525da11f6'.decode('hex')
# initialize a socket, think of it as a cable
# SOCK_DGRAM specifies that this is UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
# connect the socket, think of it as connecting the cable to the address location
s.connect((IPADDR, PORTNUM))
# send the command
while True:
    s.send(PACKETDATA)
    print(PACKETDATA)
    print("close the socket")

# close the socket
s.close()
