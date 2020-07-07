# Build Process for rmtadm

## clean
> Remove build files

**OPTIONS**
* target
  * flags: -t --target
  * type: string
  * desc: Clean only one of `client` or `server`
* rm_debs
  * flags: -d --rm_debs
  * type: boolean
  * desc: Remove deb package files in the project root
```bash
set -ex # Exit on any failure
shopt -s extglob

function clean_target() {
    rm -rf ${1}/.build
}

case "$target" in
    @(client|server)) clean_target $target ;;
    !()) echo "Unrecognized option for --target" ;;
    *) clean_target client; clean_target server ;;
esac

if [[ "$rm_debs" == "true" ]]; then
    rm *.deb
fi
```

## build
> Build both client and server .deb packages

Use `mask build -t <client|server>` to build only one of the sides

**OPTIONS**
* target
  * flags: -t --target
  * type: string
  * desc: Build only one of `client` or `server`
* install_prefix
  * flags: -i --install_prefix
  * type: string
  * desc: Alternative install prefix, defaults to /usr/local

```bash
set -ex
shopt -s extglob

function build_target() {
    $MASK clean -t $1 # Make sure there's no leftovers from last time...
    $MASK build dirstructure-$1
    $MASK build ctrl_file $1
    #dpkg-deb --build ${1}/.build/ .
}

case "$target" in
    @(client|server)) build_target ${target} ;;
    !()) echo "Unknown option for --target" ;;
    *)  echo "Building Client"
        build_target client
        echo "Building Server"
        build_target server
        ;;
esac
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
    'rmtadm_connect_client.py': ('bin/',                       0o755),
    'rmtadm.py':                ('lib/python3/dist-packages/', 0o644),
    'rmtadm':                   ('bin/',                       0o755),
}

from build.dirstructure import build_dirstructure
build_dirstructure(basedir, fakeroot, install_prefix, files)

# Special Dir
os.umask(0o022)
os.makedirs(os.path.join(fakeroot, 'var/run/rmtadm'), exist_ok=True)
```
