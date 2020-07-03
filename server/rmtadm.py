#!/usr/bin/python3

import json
import os
from os import path
import subprocess
import sys

CONNECTIONS_DIR = "/var/run/rmtadm/"

def connect(client_hostname):
    client_file = path.join(CONNECTIONS_DIR, client_hostname + ".client")

    with open(client_file) as client:
        info = json.loads(client.readline().strip())

    ssh = ["ssh", 
           "-p", info["port"], 
           "-o", "UserKnownHostsFile /dev/null",
           "-o", "StrictHostKeyChecking no",
           info["username"] + "@localhost"]

    subprocess.run(ssh, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def list():
    print(os.listdir(CONNECTIONS_DIR))

