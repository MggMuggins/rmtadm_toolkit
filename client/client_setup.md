# Remote Admin Client Setup

- Create an ssh key for the user on the client
```sh
ssh-keygen
# Work through the interactive prompt
```
- Copy the client's public key (`~/.ssh/id_rsa.pub`) into `/home/remote_client/.ssh/authorized_keys` on the server.
- Copy `remote_admin`'s public key ([https://pi.lan/id_rsa.pub]) into `~/.ssh/authorized_keys`
```sh
cat ~/Downloads/id_rsa.pub ~/.ssh/authorized_keys
```
- Install openssh and set up sshd
```sh
sudo apt-get update
sudo apt-get install openssh-server
sudo systemctl status ssh
sudo ufw allow ssh # Ensure that the firewall allows traffic on 22; may not be needed
```
- Configure sshd to reduce attack surface
```
# /etc/ssh/sshd_config
PubkeyAuthentication yes
PasswordAuthentication no
```
- Remove apt update checking
```sh
# Set all the keys to 0
sudoedit /etc/apt/apt.conf.d/20auto-upgrades
```

# To open two-way tunnel:
```sh
# "Client"
ssh -N -R 0:localhost:22 remote_admin@pi.lan
# Server
ssh -p <dynamic_port> remote_user@localhost
```

# Temporary Notes:
- Client script depends `python3-parse`
- 
