# rmtadm_toolkit

The goal of this project is to provide a few simple tools and setup guides to
allow simple and easy remote administration of linux computers. The idea is to
set up a reasonably cheap linux laptop with a custom ssh config and several
tools, and provide that laptop to a computer user who is not at all technical
and probably shouldn't be in charge of administrating their own laptop. Then
the user of the toolkit can provide remote support and administration for the
client's machine without needing to connect to their client's home network or
do any network configuration.

This is a very big WIP

## Design
This project is split into client and server components, which are designed to
run on a non-technical user's computer and the admin's remote server
respectively. The client package provides a GUI application which, when run by
the non-technical user, will connect to the remote server via ssh and run
`rmtadm_connect_client.py`, and then send some info about the connection to the
server. The admin can then log into the server and use `rmtadm connect
<hostname>` to sign in to the client's machine, without allowing the client
shell acess to the server. See the setup docs in each component to see the
reccomended key/user configuration for each machine.

