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
from Window import Window
import config
import time

import gettext
from gettext import gettext as _
gettext.textdomain('firstart')


class FirstartWindow(Window):
    __gtype_name__ = "FirstartWindow"

    #__gsignals__ = {
    #    'link-status': (GObject.SignalFlags.ACTION, None, (GObject.TYPE_BOOLEAN,))
    #}

    def finish_initializing(self, builder):   # pylint: disable=E1002

        self.btnPrev = self.ui.btnPrev
        self.btnNext = self.ui.btnNext

        iconfile = config.get_data_file('media', '%s' % ('wizard1.png',))
        self.set_icon_from_file(iconfile)

        #self.maximize()
        self.set_default_size(1000, 600)

    def translate(self):
        self.set_title(_('First Start Assistant'))
        self.ui.lblDescription.set_text('')
        self.ui.btnPrev.set_label(_('Previous'))
        self.ui.btnNext.set_label(_('Next'))

    def on_delete_event(self, widget, data=None):
        self.ungrab()
        return False

    def on_btnNext_clicked(self, widget):
        self.ungrab()
        self.destroy()

    def on_show(self, widget):
        self.grab()

    def on_grab_broken_event(self, widget, event, user_data):
        print 'on_grab_broken_even't
        print widget, event, user_data
        self.grab()

    def grab(self):
        w = self.get_window()
        i = 0
        while i < 10:
            i = i + 1
            r = Gdk.keyboard_grab(w, False, 0L)
            print r
            if r == Gdk.GrabStatus.SUCCESS:
                break
            time.sleep(1)
        r = Gdk.pointer_grab(w, True, 0, w, None, 0L)
        print r

    def ungrab(self):
        r = Gdk.keyboard_ungrab(0L)
        print r
        r = Gdk.pointer_ungrab(0L)
        print r
