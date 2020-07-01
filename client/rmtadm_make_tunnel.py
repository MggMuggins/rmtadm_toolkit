#!/usr/bin/python3

import json
import logging
from os import getuid
import parse
from pwd import getpwuid
from subprocess import PIPE, Popen
import signal
import socket
import sys
from time import sleep

def get_port_from(stream):
    """
    Read the ssh port response to determine what port the admin should
    connect to on the server
    """
    fmt = "Allocated port {} for remote forward to {}:{}"
    
    line = stream.readline().decode()
    
    rslt = parse.parse(fmt, line.strip())
    if rslt is None:
        line = stream.readline().decode()
        rslt = parse.parse(fmt, line)
    return rslt[0]


proc = Popen(
    ["ssh", "-R", "0:localhost:22", "remote_client@pi.lan"],
    stdout=sys.stdout,
    stdin=PIPE,
    stderr=PIPE,
)

info = {
    "hostname": socket.gethostname(),
    "port": get_port_from(proc.stderr),
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
    proc.send_signal(signal.SIGINT)
signal.signal(signal.SIGINT, send_sigint_to_connect_client)

for line in iter(proc.stderr.readline, b''):
    sys.stderr.write(line.decode())
    sys.stderr.flush()

