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


def firstboot_is_running():
    import subprocess

    # Don't execute this assistant if gecos-firstboot is running
    stdout = subprocess.Popen('/usr/bin/env pgrep firstboot', shell=True, stdout=subprocess.PIPE).stdout
    s_pid = stdout.read().strip()
    if len(s_pid) > 0:
        return True

    return False


def dbusservice():

    if firstboot_is_running():
        return

    import os
    from dbus.DBusService import DBusService

    s = DBusService()
    s.start()

    try:
        os.unlink('/etc/init/firstart.conf')

    except Exception as e:
        pass

    try:
        os.unlink('/etc/dbus-1/system.d/org.guadalinex.firstart.conf')

    except Exception as e:
        pass


def main():

    if firstboot_is_running():
        return

    from gi.repository import Gtk
    from firstart_lib.FirstartEntry import FirstartEntry
    from assistant.FirstartWindow import FirstartWindow

    entry = FirstartEntry()
    if entry.get_firstart() == True:
        return

    entry.set_firstart(1)

    w = FirstartWindow()
    w.show()
    Gtk.main()
