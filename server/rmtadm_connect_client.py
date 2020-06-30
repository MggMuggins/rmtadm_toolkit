#!/usr/bin/python3

from os import path, remove
import sys
import time

client = sys.argv[1]

print("Client dialed in as {}".format(client), file=sys.stderr)

port = sys.stdin.readline()

print("Recieved port: {}".format(port), file=sys.stderr)

client_file = path.join("/var/run/remote_admin/", client + ".client")
with open(client_file, "w") as client_fd:
    client_fd.write(port)

print("Client file written, waiting for interrupt", file=sys.stderr)

sys.stdin.readline() # Any more input on stdin is an indication to quit
remove(client_file) # No longer connected

