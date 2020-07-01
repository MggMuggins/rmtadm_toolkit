#!/usr/bin/python3

import gi
import signal
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk

def check_tunnel(tunnel, image):
    if tunnel.poll() is not None:
        image.set_from_file('/usr/local/share/rmtadm/client_disconnected.png')
    else:
        image.set_from_file('/usr/local/share/rmtadm/client_connected.png')
    return True  # Apparently the timeout gets destroyed if we return false

tunnel = subprocess.Popen(['/usr/local/bin/rmtadm_make_tunnel.py'])

window = Gtk.Window()
window.set_default_size(200, 200)
window.set_title("rmtadm")
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

