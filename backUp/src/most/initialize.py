# add the most.voip library root dir to the current python path...
import sys
sys.path.append("src/")

# import the Voip Library
from most.voip.api import VoipLib

# instanziate the lib
my_voip = VoipLib()

voip_params = {  u'username': u'1001',  # a name describing the user
                 u'sip_server_address': u'192.168.1.102',  # the ip of the remote sip server (default port: 5060)
                 u'sip_server_user': u'1001', # the username of the sip account
                 u'sip_server_pwd': u'1001',  #  the password of the sip account
                 u'sip_server_transport' :u'udp', # the transport type (default: tcp)
                 u'log_level' : 1,  # the log level (greater values provide more informations)
                 u'debug' : False  # enable/disable debugging messages
                 }

def notify_events(voip_event_type, voip_event, params):
    print "Received Event Type:%s -> Event: %s Params: %s" % (voip_event_type, voip_event, params)

flag=my_voip.init_lib(voip_params, notify_events)
print(flag)

flag=my_voip.register_account()
print(flag)

my_extension = "1234"
my_voip.make_call(my_extension)

import time
# wait until the call is active
while(True):
    time.sleep(1)
