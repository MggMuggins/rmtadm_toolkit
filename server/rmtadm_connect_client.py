#!/usr/bin/python3

import json
from os import path, remove
import sys
import time

print("Client dialed in")

info_raw = sys.stdin.readline()
info = json.loads(info_raw)

print("Recieved info: {}".format(info), file=sys.stderr)

client_file = path.join("/var/run/rmtadm/", info["hostname"] + ".client")
with open(client_file, "w") as client_fd:
    client_fd.write(info_raw)

print("Client file written, waiting for interrupt", file=sys.stderr)

sys.stdin.readline() # Any more input on stdin is an indication to quit
remove(client_file) # No longer connected

