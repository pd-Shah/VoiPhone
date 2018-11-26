from pyshark import LiveCapture
def NetCap():
    print ('capturing...')
    livecapture = pyshark.LiveCapture(interface="enp0s31f6", output_file='/home/pd/gits/voiphone/')
    livecapture.sniff(packet_count=10)
    print ('end of capture.')
    print (livecapture)

if __name__ == "__main__":
    NetCap()
