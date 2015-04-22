# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2013 Ross Karchner ross@karchner.com
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk, WebKit # pylint: disable=E0611
import logging
logger = logging.getLogger('kicktext')

from kicktext_lib import Window
from kicktext.AboutKicktextDialog import AboutKicktextDialog
from kicktext.PreferencesKicktextDialog import PreferencesKicktextDialog
from kicktext import controllers

# See kicktext_lib.Window.py for more details about how this class works
class KicktextWindow(Window):
    __gtype_name__ = "KicktextWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(KicktextWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutKicktextDialog
        self.PreferencesDialog = PreferencesKicktextDialog

        # Code for other initialization actions should be added here.
        self.controller = controllers.DocumentController(self)
        self.webview = WebKit.WebView()
        self.scroller = self.builder.get_object('scrollbox')
        self.scroller.add(self.webview)
        self.webview.show()

    def on_mnu_open_activate(self, menuitem, user_data=None):
        chooser = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = chooser.run()

        if response == Gtk.ResponseType.OK:
            self.controller.watch_file(chooser.get_filename(), self.webview)
        chooser.destroy()
