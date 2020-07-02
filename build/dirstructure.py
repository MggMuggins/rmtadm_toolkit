import os
from os import path
import shutil

# Iterate through a dict of filenames (in the current dir)
# mapped to pairs of target dir and mode
# Copies each file to the target dir with the given mode
# Default perms for files are 755 for dirs and 644 for files
def build_dirstructure(basedir, fakeroot, files):
    print(f"Building dirstructure in: {basedir}/{fakeroot}")

    os.umask(0o022)
    fakeroot = path.join(basedir, fakeroot)
    os.makedirs(fakeroot, exist_ok=True)

    for filename, (parent, mode) in files.items():
        dest_dir = path.join(fakeroot, parent)
        os.makedirs(dest_dir, exist_ok=True)
        
        src_file = path.join(basedir, filename)
        dest_file = path.join(dest_dir, filename)

        print(f"File: {dest_file} ({mode:o})")

        shutil.copy(src_file, dest_file)
        os.chmod(dest_file, mode)

