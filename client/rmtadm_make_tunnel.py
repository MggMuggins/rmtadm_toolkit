#!/usr/bin/python3

import json
import logging
from os import getuid
from pwd import getpwuid
from subprocess import PIPE, Popen
import signal
import sys
from time import sleep

proc = Popen(
    ["ssh", "-R", "0:localhost:22", "remote_admin@pi.lan", "rmtadm_connect_client.py todd"],
    stdout=sys.stdout,
    stdin=PIPE,
    stderr=PIPE,
)

stderr = proc.stderr.readline().decode()
print(stderr) # ssh dynamic port assignment response

info = {
    "port": stderr.split()[2].strip(),
    "username": getpwuid(getuid()).pw_name,
}
info = json.dumps(info)
print(f"Client Info: {info}")

proc.stdin.write(info.encode() + b"\n")
proc.stdin.flush()

print('Info sent to server')

# Kill the server connect_client process when we exit
def send_sigint_to_connect_client(_, __):
    proc.stdin.write("SIGINT\n".encode())
    proc.stdin.flush()
signal.signal(signal.SIGINT, send_sigint_to_connect_client)

for line in iter(proc.stderr.readline, b''):
    sys.stderr.write(line.decode())
    sys.stderr.flush()

