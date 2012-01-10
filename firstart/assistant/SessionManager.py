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


import os
import dbus
import syslog


SM_DBUS_SERVICE = 'org.gnome.SessionManager'
SM_DBUS_OBJECT_PATH = '/org/gnome/SessionManager'
SM_DBUS_CLIENT_PRIVATE_PATH = 'org.gnome.SessionManager.ClientPrivate'
sm_client_id = None


class SessionManager:

    def __init__(self, client_name):

        self.state = 0
        self.sm_proxy = None
        self.sm_client = None
        self.sm_client_id = None
        self.sm_client_name = client_name
        self.inhibit_cookie = None
        self.desktop_autostart_id = os.getenv('DESKTOP_AUTOSTART_ID')

    def log(self, message, priority=syslog.LOG_INFO):
        syslog.syslog(priority, message)

    def start(self):
        if self.state == 1:
            return

        if self.desktop_autostart_id is None:
            log('This script is intended to be executed from xdg-autostart, \
inside a gnome-session context.', syslog.LOG_ERR)
            #return False
            self.desktop_autostart_id = 0

        #DBusGMainLoop(set_as_default = True)

        session_bus = dbus.SessionBus()
        self.sm_proxy = session_bus.get_object(SM_DBUS_SERVICE, SM_DBUS_OBJECT_PATH)

        try:
            self.register_client()
            #self.connect_signals()
            self.inhibit()
            self.state = 1

        except Exception as e:
            self.log(str(e), syslog.LOG_ERR)

    def stop(self):
        if self.state == 0:
            return
        try:
            self.uninhibit()
            self.unregister_client()
        except Exception as e:
            self.log(str(e), syslog.LOG_ERR)

    def register_client(self):
        register_client = self.sm_proxy.get_dbus_method('RegisterClient', SM_DBUS_SERVICE)
        self.sm_client_id = register_client(self.sm_client_name, self.desktop_autostart_id)
        self.log('Client Id: ' + str(self.sm_client_id))

    def unregister_client(self):
        unregister_client = self.sm_proxy.get_dbus_method('UnregisterClient', SM_DBUS_SERVICE)
        unregister_client(self.sm_client_id)

    def connect_signals(self):
        session_bus = dbus.SessionBus()
        self.sm_client = session_bus.get_object(SM_DBUS_SERVICE, self.sm_client_id)
        #self.sm_client.connect_to_signal('QueryEndSession', self.on_query_end_session)
        #self.sm_client.connect_to_signal('EndSession', self.on_end_session)
        #self.sm_client.connect_to_signal('CancelEndSession', self.on_cancel_end_session)

    def inhibit(self):
        if self.inhibit_cookie != None:
            return
        m_inhibit = self.sm_proxy.get_dbus_method('Inhibit', SM_DBUS_SERVICE)
        self.inhibit_cookie = m_inhibit(self.sm_client_name, 0, 'Reason', 4)
        self.log('Inhibit cookie: ' + str(self.inhibit_cookie))

    def uninhibit(self):
        if self.inhibit_cookie == None:
            return
        m_uninhibit = self.sm_proxy.get_dbus_method('Uninhibit', SM_DBUS_SERVICE)
        m_uninhibit(self.inhibit_cookie)
        self.inhibit_cookie = None

