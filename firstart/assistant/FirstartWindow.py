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


from gi.repository import Gdk
from gi.repository import WebKit as webkit
from firstart_lib.Window import Window
from firstart.dbus.DBusClient import DBusClient
import firstart_lib.config as config
from SessionManager import SessionManager
import time

import gettext
from gettext import gettext as _
gettext.textdomain('firstart')

GECOS_INFO_URI = 'file:///usr/share/guadalinex-firstart/index.html'
GECOS_BLOCKED_URI = 'file:///usr/share/guadalinex-firstart/block.html'
GECOS_UNBLOCKED_URI = 'file:///usr/share/guadalinex-firstart/unblock.html'

DBC_STATE_STOPPED = 0
DBC_STATE_RUNNING = 1
DBC_STATE_FINISHED = 2


class FirstartWindow(Window):

    __gtype_name__ = "FirstartWindow"

    def finish_initializing(self, builder):   # pylint: disable=E1002

        iconfile = config.get_data_file('media', '%s' % ('wizard1.png',))
        self.set_icon_from_file(iconfile)

        self.ui.btnTest.set_visible(False)
        self.ui.btnClose.set_sensitive(False)

        #self.maximize()
        self.resize(1000, 700)
        #self.fullscreen()

        self.sm = SessionManager('gecos-firstart')
        self.sm.start()
        self.show_browser()

        self.dbusclient = DBusClient()
        self.dbusclient.connect('state-changed', self.on_dbusclient_state_changed)

        try:
            self.dbusclient.start()
            state = self.dbusclient.get_state(reply_handler=self.reply_handler, error_handler=self.error_handler)

        except Exception as e:
            self.unblock()

    def show_browser(self):
        self.webview = webkit.WebView()
        self.ui.scContent.add(self.webview)
        self.webview.load_uri(GECOS_BLOCKED_URI)
        self.webview.show()

    def reply_handler(self, state):
        if state == DBC_STATE_FINISHED:
            self.unblock()

    def error_handler(self, e):
        self.unblock()

    def translate(self):
        self.set_title(_('Guadalinex GECOS Guide'))
        self.ui.lblInfo.set_label(_('You can take a look at the latest news while your system is being configured ...'))
        self.ui.btnTest.set_label(_('Test'))
        self.ui.btnClose.set_label(_('Close'))

    def on_delete_event(self, widget, data=None):
        self.ungrab()
        return False

    def on_btnTest_clicked(self, widget):
        self.sm.stop()
        self.ungrab()
        self.destroy()

    def on_btnClose_clicked(self, widget):
        self.sm.stop()
        self.ungrab()
        self.destroy()

    def on_show(self, widget):
        self.grab()

    def on_grab_broken_event(self, widget, event, user_data):
        self.grab()

    def on_dbusclient_state_changed(self, sender, state):
        if state == DBC_STATE_STOPPED:
            #print 'stopped...'
            pass

        elif state == DBC_STATE_RUNNING:
            #print 'running...'
            pass

        elif state == DBC_STATE_FINISHED:
            self.unblock()

    def unblock(self):
        self.ui.btnClose.set_sensitive(True)
        self.ui.lblInfo.set_label(_('Your system has been configured.'))

    def grab(self):
        #return
        w = self.get_window()
        i = 0
        while i < 10:
            i = i + 1
            r = Gdk.keyboard_grab(w, False, 0L)
            #print r
            if r == Gdk.GrabStatus.SUCCESS:
                break
            time.sleep(1)
        r = Gdk.pointer_grab(w, True, 0, w, None, 0L)
        #print r

    def ungrab(self):
        r = Gdk.keyboard_ungrab(0L)
        r = Gdk.pointer_ungrab(0L)
