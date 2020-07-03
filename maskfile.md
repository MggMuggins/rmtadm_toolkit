# Build Process for rmtadm

## clean
> Remove build files

**OPTIONS**
* rm_debs
  * flags: -d --rm_debs
  * type: boolean
  * desc: Remove deb package files in the project root
```bash
set -x

rm -r client/.build
rm -r server/.build

if [[ "$rm_debs" == "true" ]]; then
    rm *.deb
fi
```

## build
> Build both client and server .deb packages

**OPTIONS**
* install_prefix
  * flags: -i --install_prefix
  * type: string
  * desc: Alternative install prefix, defaults to /usr/local

```bash
echo Building Client
$MASK build target client
echo Building Server
$MASK build target server
```

### build client
> Alias for `mask build target client`

**OPTIONS**
* install_prefix
  * flags: -i --install_prefix
  * type: string
  * desc: Alternative install prefix, defaults to /usr/local
```bash
$MASK build target client
```

### build server
> Alias for `mask build target server`

**OPTIONS**
* install_prefix
  * flags: -i --install_prefix
  * type: string
  * desc: Alternative install prefix, defaults to /usr/local
```bash
$MASK build target server
```

### build target (target)
> Build a `.deb` package to perform setup operations for `target = (client|server)`

**OPTIONS**
* install_prefix
  * flags: -i --install_prefix
  * type: string
  * desc: Alternative install prefix, defaults to /usr/local
```bash
set -ex # Exit on any failure

$MASK build dirstructure-$target
$MASK build ctrl_file $target
dpkg-deb --build ${target}/.build/ .
```

### build ctrl_file (target)
> Generate the control file for either the `client` or the `server`

Very likely this will never be invoked manually
```bash
set -ex

mkdir -p ${target}/.build/DEBIAN
cp build/common.ctrl ${target}/.build/DEBIAN/control
cat build/${target}.ctrl >> ${target}/.build/DEBIAN/control
```

### build dirstructure-client
> Map files to fs locations in the fakeroot for the client deb

Very likely this will never be invoked manually
```python3
import os

basedir = 'client'

fakeroot = 'client/.build'

install_prefix = os.environ.get('install_prefix', '/usr/local/')

files = {
    'rmtadm_make_tunnel.py':   ('bin/',                0o755),
    'rmtadm_window.py':        ('bin/',                0o755),
    'rmtadm.desktop':          ('share/applications/', 0o644),
    'gearhead.png':            ('share/rmtadm/',       0o644),
    'client_connected.png':    ('share/rmtadm/',       0o644),
    'client_disconnected.png': ('share/rmtadm/',       0o644),
}

from build.dirstructure import build_dirstructure
build_dirstructure(basedir, fakeroot, install_prefix, files)
```

### build dirstructure-server
> Map files to fs locations in the fakeroot for the server deb

Very likely this will never be invoked manually
```python3
import os

basedir = 'server'

fakeroot = 'server/.build'

install_prefix = os.environ.get('install_prefix', '/usr/local/')

files = {
    'rmtadm_connect_client.py': ('bin/', 0o755),
    'rmtadm_connect.py':        ('bin/', 0o755),
}

from build.dirstructure import build_dirstructure
build_dirstructure(basedir, fakeroot, install_prefix, files)

# Special Dir
os.umask(0o022)
os.makedirs(os.path.join(fakeroot, 'var/run/rmtadm'), exist_ok=True)
```
