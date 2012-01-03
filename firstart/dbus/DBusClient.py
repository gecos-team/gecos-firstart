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


from gi.repository import GObject
import dbus
from dbus.mainloop.glib import DBusGMainLoop


DBUS_SERVICE = 'org.guadalinex.firstart'
DBUS_OBJECT_PATH = '/org/guadalinex/firstart'


class DBusClient(GObject.GObject):

    __gtype_name__ = 'DBusClient'

    __gsignals__ = {
        'state-changed': (GObject.SignalFlags.ACTION, None, (int,)),
    }

    def __init__(self):
        GObject.GObject.__init__(self)

    def start(self):
        DBusGMainLoop(set_as_default=True)
        self.bus = None
        self.proxy = None

        self.bus = dbus.SystemBus()
        self.proxy = self.bus.get_object(DBUS_SERVICE, DBUS_OBJECT_PATH)
        self.proxy.connect_to_signal('StateChanged', self.on_state_changed)

    def get_state(self, reply_handler, error_handler):
        m_get_state = self.proxy.get_dbus_method('get_state', DBUS_SERVICE)
        state = m_get_state(reply_handler=reply_handler, error_handler=error_handler)
        return state

    def on_state_changed(self, state):
        self.emit('state-changed', state)
