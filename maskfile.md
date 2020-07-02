# Build Process for rmtadm

## clean
> Remove build files

**OPTIONS**
* rm-debs
  * flags: -d --rm-debs
  * type: boolean
  * desc: Remove deb package files in the project root
```bash
rm -r client/.build
rm -r server/.build

if [[ "$rm-debs" == "true" ]]; then
    rm *.deb
fi
```

## build
> Build both client and server .deb packages
```bash
echo Building Client
$MASK build target client
echo Building Server
$MASK build target server
```

### build client
> Alias for `mask build target client`
```bash
$MASK build target client
```

### build server
> Alias for `mask build target server`
```bash
$MASK build target server
```

### build target (target)
> Build a `.deb` package to perform setup operations for `target = (client|server)`

```bash
$MASK build dirstructure-$target
$MASK build ctrl_file $target
dpkg-deb --build ${target}/.build/ .
```

### build ctrl_file (target)
> Generate the control file for either the `client` or the `server`

Very likely this will never be invoked manually
```bash
mkdir -p ${target}/.build/DEBIAN
cp build/common.ctrl ${target}/.build/DEBIAN/control
cat build/${target}.ctrl >> ${target}/.build/DEBIAN/control
```

### build dirstructure-client
> Map files to fs locations and copy them into the fakeroot for the client deb

Very likely this will never be invoked manually
```python3
basedir = 'client'

fakeroot = '.build'

files = {
    'rmtadm_make_tunnel.py':   ('usr/local/bin/',                0o755),
    'rmtadm_window.py':        ('usr/local/bin/',                0o755),
    'rmtadm.desktop':          ('usr/local/share/applications/', 0o644),
    'gearhead.png':            ('usr/local/share/rmtadm/',       0o644),
    'client_connected.png':    ('usr/local/share/rmtadm/',       0o644),
    'client_disconnected.png': ('usr/local/share/rmtadm/',       0o644),
}

from build.dirstructure import build_dirstructure
build_dirstructure(basedir, fakeroot, files)
```

### build dirstructure-server
```bash
echo UNIMPLEMENTED
```
