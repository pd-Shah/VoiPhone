#!/bin/bash
fuser -k 5060/udp
fuser -k 9090/udp
fuser -k 20000/udp
fuser -k 19000/udp
service asterisk restart
