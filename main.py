# add the most.voip library root dir to the current python path...
import sys
sys.path.append("src/")
from most.voip.api import VoipLib
from most.voip.constants import VoipEvent


import time, sys


if __name__ == '__main__':

    # choose a sip extension to call
    extension = "steand"

    # implement a method that will capture all the events triggered by the Voip Library
    def notify_events(voip_event_type,voip_event, params):
        print "Received event type:%s Event:%s -> Params: %s" % (voip_event_type, voip_event, params)

        # event triggered when the account registration has been confirmed by the remote Sip Server
        if (voip_event==VoipEvent.ACCOUNT_REGISTERED):
            print "Making a call dialing the extension: %s" % extension
            myVoip.make_call(extension)

        # event  triggered when a call has been established
        elif(voip_event==VoipEvent.CALL_ACTIVE):
            print "The call with %s has been established"  % myVoip.get_call().get_remote_uri()

        # events triggered when the call ends for some reasons
        elif (voip_event in [VoipEvent.CALL_REMOTE_DISCONNECTION_HANGUP, VoipEvent.CALL_REMOTE_HANGUP, VoipEvent.CALL_HANGUP]):
            print "End of call. Destroying lib..."
            myVoip.destroy_lib()

        # event triggered when the library was destroyed
        elif (voip_event==VoipEvent.LIB_DEINITIALIZED):
            print "Lib Destroyed. Exiting from the app."
            sys.exit(0)

        # just print informations about other events triggered by the library
        else:
            print "Received unhandled event type:%s --> %s" % (voip_event_type,voip_event)

    voip_params = {u'username': u'steand',
                   u'sip_server_pwd': u'steand',
                   u'sip_server_address': u'192.168.0.102' ,
                   u'sip_server_user': u'steand',
                   u'sip_server_transport' :u'udp',
                   # u'turn_server_address': u'192.168.1.79',
                   #u'turn_server_user': u'',
                   #u'turn_server_pwd': u'',
                   u'log_level' : 1,
                   u'debug' : True }



    myVoip = VoipLib()
    print "Initializing the Voip Lib..."
    myVoip.init_lib(voip_params, notify_events)
    print "Registering the account on the Sip Server..."
    myVoip.register_account()

    while True:
        time.sleep(10)
    # myVoip.hangup_call()
