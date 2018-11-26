import socket
from time import sleep
def client():
    # I change second packet to 2packet for visually distinguish the packets
    packet = "<packet></packet>\0<2packet></2packet>"
    HOST, PORT = '192.168.0.102', 5060
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect((HOST, PORT))
    while True:
        try:
            sock.send(packet)
            sleep(1)
            # this is the problem here
            reply = sock.recv(131072)
            if not reply:
                break
            print "recvd: ", reply
        except KeyboardInterrupt:
            print "bye"
            break
    sock.close()
    return reply
