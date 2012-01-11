#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# This file is part of Guadalinex
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__ = "Antonio Hernández <ahernandez@emergya.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys
import glob

try:
    import DistUtilsExtra.auto
    from distutils.core import setup, Command
    from DistUtilsExtra.command import *
except ImportError:
    print >> sys.stderr, 'To build firstart you need https://launchpad.net/python-distutils-extra'
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.18', 'needs DistUtilsExtra.auto >= 2.18'


def update_config(values={}):

    oldvalues = {}
    try:
        fin = file('firstart_lib/config.py', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split(' = ')  # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = %s\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find firstart_lib/config.py")
        sys.exit(1)
    return oldvalues


def update_upstart_script(values={}):

    oldvalues = {}
    try:
        fin = file('data/etc/init/firstart.conf', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            fields = line.split('=')  # Separate variable from value
            if fields[0].strip() in values:
                oldvalues[fields[0].strip()] = fields[1].strip()
                line = "%s=%s\n" % (fields[0], values[fields[0].strip()])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find data/etc/init/firstart.conf.in")
        sys.exit(1)
    return oldvalues


def update_autostart_script(values={}):

    oldvalues = {}
    try:
        fin = file('data/etc/xdg/autostart/firstart.desktop', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            for key in values:
                if key in line:
                    value = values[key].replace("'", '')
                    oldvalues[value] = key
                    line = line.replace(key, value)
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find data/etc/xdg/autostart/firstart.desktop.in")
        sys.exit(1)
    return oldvalues


def update_desktop_file(datadir):

    try:
        fin = file('firstart.desktop.in', 'r')
        fout = file(fin.name + '.new', 'w')

        for line in fin:
            if 'Icon=' in line:
                line = "Icon=%s\n" % (datadir + 'media/wizard1.png')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError), e:
        print ("ERROR: Can't find firstart.desktop.in")
        sys.exit(1)


def copy_pages(pages_path):
    pass


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        values = {'__firstart_data_directory__': "'%s'" % (
                                        self.prefix + '/share/firstart/'),
                  '__version__': "'%s'" % self.distribution.get_version(),
                  '__firstart_prefix__': "'%s'" % self.prefix}
        previous_values = update_config(values)
        #update_desktop_file(self.prefix + '/share/firstart/')
        upstart_bak = update_upstart_script(values)
        autostart_bak = update_autostart_script(values)

        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)
        update_upstart_script(upstart_bak)
        update_autostart_script(autostart_bak)


class Clean(Command):
    description = "custom clean command that forcefully removes dist/build directories and update data directory"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./build ./dist')
        update_data_path(prefix, oldvalue)


##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='firstart',
    version='0.0.2',
    license='GPL-2',
    author='Antonio Hernández',
    author_email='ahernandez@emergya.com',
    description='First start assistant for Guadalinex GECOS',
    url='https://github.com/gecos-team/gecos-firstart',

    keywords=['python', 'gnome', 'guadalinex', 'gecos'],

    packages=[
        'firstart',
        'firstart_lib',
        'firstart.assistant',
        'firstart.dbus'
    ],

    package_dir={
        'firstart': 'firstart',
        'firstart_lib': 'firstart_lib',
        'firstart.assistant': 'firstart/assistant',
        'firstart.dbus': 'firstart/dbus'
    },

    scripts=[
        'bin/firstart',
        'bin/firstart-dbusservice'
    ],

    data_files=[
       ('share/firstart/media', glob.glob('data/media/*')),
       ('share/firstart/ui', glob.glob('data/ui/*')),
       ('share/guadalinex-firstart', glob.glob('data/usr/share/guadalinex-firstart/*')),
       ('/etc/xdg/autostart', glob.glob('data/etc/xdg/autostart/firstart.desktop')),
       ('/etc/init', glob.glob('data/etc/init/firstart.conf')),
       ('/etc/dbus-1/system.d', glob.glob('data/etc/dbus-1/system.d/org.guadalinex.firstart.conf'))
    ],

    cmdclass={
        'install': InstallAndUpdateDataDirectory,
        "build": build_extra.build_extra,
        "build_i18n":  build_i18n.build_i18n,
        "clean": [clean_i18n.clean_i18n, Clean],
    }
)
