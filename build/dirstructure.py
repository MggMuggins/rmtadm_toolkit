import os
from os import path
import shutil

# Iterate through a dict of filenames (in the current dir)
# mapped to pairs of target dir and mode
# Arguments: (leaving one of the first three empty means to use the cwd)
#   basedir - - - - - directory from which to get each filename
#   fakeroot  - - - - directory in which to build the package directory structure
#   install_prefix  - directory to be prepended to each target path
#   files - - - - - - dict {
#                         #                                    fakeroot/install_prefix       mode
#                         "filename/relative/to/basedir": ("install/path/relative/to/above", 0o644),
#                     }
def build_dirstructure(basedir, fakeroot, install_prefix, files, umask=0o022):

    os.umask(umask)
    os.makedirs(fakeroot, exist_ok=True)

    # It makes sense to notate install_prefix relative to root, but don't use it that way
    install_prefix = strip_root(install_prefix)

    print(f"Building dirstructure in: {fakeroot}") 

    for filename, (parent, mode) in files.items():
        dest_dir = path.join(fakeroot, install_prefix, parent)
        os.makedirs(dest_dir, exist_ok=True)
        
        src_file = path.join(basedir, filename)
        dest_file = path.join(dest_dir, filename)

        print(f"File: {dest_file} ({mode:o})")

        shutil.copy(src_file, dest_file)
        os.chmod(dest_file, mode)

# Unintelligently turn an absolute path to a relative one
def strip_root(path):
    if path.startswith('/'):
        return path[1:]
    else:
        return path

