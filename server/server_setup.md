# Remote Admin Server Setup

- Create a user `remote_admin`
```sh
sudo adduser remote_admin
```
- Create an ssh key for the `remote_admin` user
```sh
ssh-keygen
```
- Copy `remote_admin`'s public key to `~/.ssh/authorized_keys` on the client
- Create a user `remote_client`
```sh
sudo adduser --disabled-password --shell /usr/local/bin/rmtadm_connect_client.py remote_client
```
- Ensure that `remote_client`'s `~/.ssh/authorized_keys` includes the key of each client user, with the following options:
```
command="/usr/local/bin/rmtadm_connect_client.py",no-pty ssh-rsa ...... user@hostname
```
- Ensure that `/var/run/rmtadm` exists and that `remote_client` has rwx access.

