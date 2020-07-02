#!/usr/bin/python3

import json
from os import path
import subprocess
import sys

if len(sys.argv) < 2:
    print("Please provide a client hostname")
    exit(1)

client_file = path.join("/var/run/rmtadm/", sys.argv[1] + ".client")

with open(client_file) as client:
    info = json.loads(client.readline().strip())

ssh = ["ssh", 
       "-p", info["port"], 
       "-o", "UserKnownHostsFile /dev/null",
       "-o", "StrictHostKeyChecking no",
       info["username"] + "@localhost"]

subprocess.run(ssh, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

