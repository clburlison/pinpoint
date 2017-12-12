#!/usr/bin/python
"""Build pinpoint package."""

import os
import sys
import plistlib
import subprocess
import tempfile
import fnmatch

from xml.parsers.expat import ExpatError


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PKGBUILD = "/usr/bin/pkgbuild"
PRODUCTBUILD = "/usr/bin/productbuild"
PRODUCTSIGN = "/usr/bin/productsign"
SIGNING_IDENTITY = "Developer ID Installer: Clayton Burlison (RP82Y2QL76)"

class PkgError(Exception):
    '''Base Exception for errors in this domain'''
    pass


class BuildError(PkgError):
    '''Exception for build errors'''
    pass


def display(message, quiet=False):
    """Print message to stdout unless quiet is True."""
    if not quiet:
        toolname = os.path.basename(sys.argv[0])
        print "%s: %s" % (toolname, message)


def generate_dist_info(version, dist_path):
    """Generate a Distribution file with current app versions."""
    with open(os.path.join(CURRENT_DIR,
                           'Distribution-Template'), 'r') as the_file:
        filedata = the_file.read()

    # Replace the target string
    filedata = filedata.replace('replace_version', version)

    # Write the file out again
    with open(dist_path, 'w') as the_file:
        the_file.write(filedata)


def generate_component(tmpdir):
    """Generate a component file and supress bundle relocation."""
    component_plist = os.path.abspath(os.path.join(tmpdir, 'component.plist'))
    payload_path = os.path.abspath(os.path.join(CURRENT_DIR, 'payload'))
    cmd = [PKGBUILD, '--analyze', '--root', payload_path, component_plist]
    try:
        returncode = subprocess.call(cmd)
    except OSError, err:
        raise BuildError(
            "pkgbuild execution failed with error code %d: %s"
            % (err.errno, err.strerror))
    if returncode:
        raise BuildError(
            "pkgbuild failed with exit code %d: %s"
            % (returncode, " ".join(str(err).split())))

    # Supress bundle relocation
    try:
        plist = plistlib.readPlist(component_plist)
    except ExpatError, err:
        raise BuildError("Couldn't read %s" % component_plist)
    # plist is an array of dicts, iterate through
    for bundle in plist:
        if bundle.get("BundleIsRelocatable"):
            bundle["BundleIsRelocatable"] = False
            display('Turning off bundle relocation for %s'
                    % bundle['RootRelativeBundlePath'])
    try:
        plistlib.writePlist(plist, component_plist)
    except BaseException, err:
        raise BuildError("Couldn't write %s" % component_plist)
    return component_plist


def make_pkginfo(tmpdir):
    """Create a stub PackageInfo file for use with pkgbuild."""
    pkginfo_path = os.path.abspath(os.path.join(tmpdir, 'PackageInfo'))
    pkginfo_text = ('<?xml version="1.0" encoding="utf-8" standalone="no"?>'
                    '<pkg-info postinstall-action="none"/>')
    try:
        fileobj = open(pkginfo_path, mode='w')
        fileobj.write(pkginfo_text)
        fileobj.close()
        return pkginfo_path
    except (OSError, IOError), err:
        raise BuildError('Couldn\'t create PackageInfo file: %s' % err)


def remove_ds_store(path):
    """Remove .DS_Store files from package payload."""
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '.DS_Store'):
            file_path = os.path.join(root, filename)
            display('Remove DS_Store from: {}'.format(file_path))
            os.remove(file_path)


def build_comp_pkg(pkg_name, version, pkg_id, pkg_info, component_plist):
    """Build a component package."""
    display('Build component package')
    comp_pkg = os.path.abspath(os.path.join(CURRENT_DIR, '{}.pkg'.format(pkg_name)))
    payload_path = os.path.abspath(os.path.join(CURRENT_DIR, 'pkgroot'))
    scripts_path = os.path.abspath(os.path.join(CURRENT_DIR, 'scripts'))
    remove_ds_store(payload_path)
    remove_ds_store(scripts_path)
    cmd = [PKGBUILD, '--ownership', 'recommended',
           '--identifier', pkg_id,
           '--version', version, '--info', pkg_info,
           '--root', payload_path, '--install-location', '/',
           '--component-plist', component_plist,
           '--scripts', scripts_path, comp_pkg]
    retcode = subprocess.call(cmd)
    if retcode:
        raise BuildError("Package creation failed.")
    return comp_pkg


def build_dist_pkg(pkg_name, version, dist_path):
    """Build and sign our distribution package."""
    display('Build and sign distrubtion package')
    dist_pkg_path = os.path.abspath(os.path.join(
            CURRENT_DIR, '{}-{}.pkg'.format(pkg_name, version)))
    cmd = [PRODUCTBUILD, '--distribution', dist_path,
           dist_pkg_path, '--sign',
           SIGNING_IDENTITY,
           '--timestamp']
    retcode = subprocess.call(cmd)
    if retcode:
        raise BuildError("Distribution package creation failed.")


def main():
    """Main."""
    version = sys.argv[1]
    pkg_id = sys.argv[2]
    pkg_name = sys.argv[3]
    tmpdir = tempfile.mkdtemp()
    print tmpdir
    dist_path = os.path.abspath(os.path.join(CURRENT_DIR, 'Distribution'))
    generate_dist_info(version, dist_path)
    pkg_info = make_pkginfo(tmpdir)
    component_plist = generate_component(tmpdir)
    comp_pkg = build_comp_pkg(pkg_name, version, pkg_id, pkg_info, component_plist)
    build_dist_pkg(pkg_name, version, dist_path)

    # cleanup temp data
    _ = subprocess.call(['/bin/rm', '-rf', tmpdir])
    _ = subprocess.call(['/bin/rm', '-rf', comp_pkg])
    _ = subprocess.call(['/bin/rm', '-rf', dist_path])


if __name__ == '__main__':
    main()
