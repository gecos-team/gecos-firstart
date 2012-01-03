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


from gi.repository import Gtk
from gi.repository import GObject
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import shlex
import subprocess


DBUS_SERVICE = 'org.guadalinex.firstart'
DBUS_OBJECT_PATH = '/org/guadalinex/firstart'

STATE_STOPPED = 0
STATE_RUNNING = 1
STATE_FINISHED = 2


class DBusService(dbus.service.Object):

    def __init__(self):
        self.state = STATE_STOPPED

    def start(self):
        DBusGMainLoop(set_as_default=True)
        self.bus_name = dbus.service.BusName(DBUS_SERVICE, bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, self.bus_name, DBUS_OBJECT_PATH)

        self.state = STATE_RUNNING

        cmd = '/usr/bin/env chef-client'
        args = shlex.split(cmd)
        self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        GObject.timeout_add_seconds(1, self.check_state)

    def check_state(self):
        s = self.process.poll()
        state_changed = s != None
        if state_changed == True:
            self.set_state(STATE_FINISHED)

        # Return True for GObject timer to continue,
        # False to stop the timer.
        return not state_changed

    def set_state(self, state):
        self.state = state
        self.StateChanged(self.state)

    @dbus.service.method(DBUS_SERVICE)
    def stop(self):
        Gtk.main_quit()

    @dbus.service.method(DBUS_SERVICE, out_signature='i')
    def get_state(self):
        return self.state

    @dbus.service.signal(DBUS_SERVICE, signature='i')
    def StateChanged(self, state):
        #print 'StateChanged', state
        pass
