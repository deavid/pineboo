# Copyright (c) 2017, Riverbank Computing Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import argparse
import os
import subprocess
import sys
import shutil
import traceback


def run(args):
    """ Run a command and terminate if it fails. """

    try:
        ec = subprocess.call(' '.join(args), shell=True)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        ec = 1

    if ec:
        sys.exit(ec)


# Parse the command line.
parser = argparse.ArgumentParser()
parser.add_argument('--no-sysroot', help="do not build the sysroot",
                    action='store_true')
parser.add_argument('--sources',
                    help="the directory containing the source packages", metavar="DIR")
parser.add_argument('--target', help="the target platform", default='')
parser.add_argument('--quiet', help="disable progress messages",
                    action='store_true')
parser.add_argument('--verbose', help="enable verbose progress messages",
                    action='store_true')
cmd_line_args = parser.parse_args()
build_sysroot = not cmd_line_args.no_sysroot
sources = cmd_line_args.sources
target = cmd_line_args.target
quiet = cmd_line_args.quiet
verbose = cmd_line_args.verbose

print("TARGET %s\n" % target)

if sources:
    sources = os.path.abspath(sources)
else:
    sources = 'src'

# Pick a default target if none is specified.
if not target:
    if sys.platform == 'win32':
        # Look for a 64-bit compiler.
        arch = '64' if os.environ.get('Platform') == 'X64' else '32'
        target = 'win-' + arch
    elif sys.platform == 'darwin':
        target = 'macos-64'
    elif sys.platform.startswith('linux'):
        import struct

        target = 'linux-{0}'.format(8 * struct.calcsize('P'))
    else:
        print("Unsupported platform:", sys.platform, file=sys.stderr)
        sys.exit(2)

# rename al files in scripts for deploy
path_ = "%s/share/pineboo/scripts" % os.path.dirname(os.path.abspath(__file__))
script_files = os.listdir(path_)
i = 1

for file_name in script_files:
    if str(file_name).endswith(".py"):
        file_name_dest = file_name.replace(".py", ".py.src")
        shutil.copy(os.path.join(path_, file_name), os.path.join(path_, file_name_dest))
    i = i + 1
# Anchor everything from the directory containing this script.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

sysroot_dir = 'sysroots/' + target
build_dir = 'builds/' + target
host_bin_dir = os.path.abspath(os.path.join(sysroot_dir, 'host', 'bin'))

# Build sysroot.
if build_sysroot:
    if not os.path.exists("sysroots"):
        os.mkdir("sysroots")

    args = ['pyqtdeploy-sysroot', '--target', target, '--sysroot', sysroot_dir,
            '--source-dir', sources]

    if quiet:
        args.append('--quiet')

    if verbose:
        args.append('--verbose')

    args.append('sysroot.json')

    run(args)
    if target == "android-32":
        try:
            os.symlink("%s/../../src/bzip2-android/lib/include/bzlib.h" % os.path.abspath(os.path.join(sysroot_dir)), "%s/include/bzlib.h" % sysroot_dir)
            os.symlink("%s/../../src/bzip2-android/lib/lib/armeabi/libbz2.so" % os.path.abspath(os.path.join(sysroot_dir)), "%s/lib/libbz2.so" % sysroot_dir)
            os.symlink("%s/../../src/sqlite3-android/build/sqlite3.h" % os.path.abspath(os.path.join(sysroot_dir)), "%s/include/sqlite3.h" % sysroot_dir)
            os.symlink("%s/../../src/sqlite3-android/obj/local/armeabi/libsqlite3.so" %
                       os.path.abspath(os.path.join(sysroot_dir)), "%s/lib/libsqlite3.so" % sysroot_dir)
        except Exception:
            print(traceback.format_exc())
    
    if target == "linux-64":
        try:
            os.symlink("%s/../../src/sqlite3-linux-64/sqlite-autoconf-3260000/sqlite3ext.h" % os.path.abspath(os.path.join(sysroot_dir)), "%s/include/sqlite3ext.h" % sysroot_dir)
            os.symlink("%s/../../src/sqlite3-linux-64/sqlite-autoconf-3260000/sqlite3.h" % os.path.abspath(os.path.join(sysroot_dir)), "%s/include/sqlite3.h" % sysroot_dir)
            os.symlink("%s/../../src/sqlite3-linux-64/sqlite-autoconf-3260000/.libs/libsqlite3.so" % os.path.abspath(os.path.join(sysroot_dir)), "%s/lib/libsqlite3.so" % sysroot_dir)
        except Exception:
            print(traceback.format_exc())
else:
    print("INFO::sysroot-%s ya existe, omitiendo ..." % target)
# Build the demo.
if not os.path.exists("builds"):
    os.mkdir("builds")
run(['pyqtdeploy-build', '--target', target, '--sysroot', sysroot_dir,
     '--build-dir', build_dir, 'pyqt-pineboo.pdy'])

# Run qmake.  Use the qmake left by pyqtdeploy-sysroot.
os.chdir(build_dir)
run([os.path.join(host_bin_dir, 'qmake')])

# Run make. (When targeting iOS we leave it to Xcode.)
if target.startswith('ios'):
    pass
else:
    # We only support MSVC on Windows.
    make = 'nmake' if sys.platform == 'win32' else 'make'

    run([make])

    if target.startswith('android'):
        run([make, 'INSTALL_ROOT=deploy', 'install'])
        #os.symlink("%s/../../build_android.xml" % os.path.abspath("deploy"),"%s/build.xml" % os.path.abspath("deploy"))
        #os.symlink("%s/../../project.properties" % os.path.abspath("deploy"), "%s/project.properties" % os.path.abspath("deploy"))
        run([os.path.join(host_bin_dir, 'androiddeployqt'), '--input',
             'android-libpineboo.so-deployment-settings.json', '--output',
             'deploy', '--deployment', 'bundled', '--android-platform', os.environ.get('ANDROID_NDK_PLATFORM'), '--gradle'])

# Tell the user where the demo is.
if target.startswith('android'):
    apk_dir = os.path.join(build_dir, 'deploy', 'build', 'outputs', 'apk')
    print("""The QtApp-debug.apk file can be found in the '{0}'
directory.  Run adb to install it to a simulator.""".format(apk_dir))

elif target.startswith('ios'):
    print("""The pyqt-demo.xcodeproj file can be found in the '{0}' directory.
Run Xcode to build the app and run it in the simulator or deploy it to a
device.""".format(build_dir))

elif target.startswith('win') or sys.platform == 'win32':
    print("The Pineboo executable can be found in the '{0}' directory.".format(
        os.path.join(build_dir, 'release')))

else:
    print("The Pineboo executable can be found in the '{0}' directory.".format(
        build_dir))

# Limpiar y completar build_dir
lstDir = os.walk(build_dir)
for root, dirs, files in lstDir:
    for fichero in files:
        (nombreFichero, extension) = os.path.splitext(fichero)
        if extension in [".o", ".h", ".cpp"]:
            os.remove(fichero)
