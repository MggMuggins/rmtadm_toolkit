#!/usr/bin/python3

import gi
from os import path
import signal
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

INSTALL_BASE_PATH = '/usr/local'

MAKE_TUNNEL = path.join(INSTALL_BASE_PATH, 'bin/rmtadm_make_tunnel.py')

CLIENT_CONNECTED = path.join(INSTALL_BASE_PATH, 'share/rmtadm/client_connected.png')
CLIENT_DISCONNECTED = path.join(INSTALL_BASE_PATH, 'share/rmtadm/client_disconnected.png')

# If the make_tunnel process has died, indicate that the client has disconnected
def check_tunnel(tunnel, image):
    # poll() looks for an exit code
    if tunnel.poll() is None:
        image.set_from_file(CLIENT_CONNECTED)
    else:
        image.set_from_file(CLIENT_DISCONNECTED)
    return True  # Apparently the timeout gets destroyed if we return false

tunnel = subprocess.Popen([MAKE_TUNNEL])

window = Gtk.Window()
window.set_default_size(200, 200)
window.set_title("Connect Remote Admin")
window.set_wmclass("rmtadm", "rmtadm")
window.connect('destroy', Gtk.main_quit)

image = Gtk.Image()
window.add(image)

# Every two seconds make sure that the tunnel is still active
GLib.timeout_add(2000, check_tunnel, tunnel, image)
check_tunnel(tunnel, image) # And check it once to begin with

image.show()
window.show()

# Make sure to kill the child process after the window is closed
Gtk.main()
tunnel.send_signal(signal.SIGINT)

