# -*- coding: utf-8 -*-

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2020, Paul Blottiere"
__date__ = "2020/04/19"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from .resources import *
from .src.gui import ProfileMapTool, SelectDock, View, Chart


def classFactory(iface):
    return MinimalPlugin(iface)


class MinimalPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        icon = QIcon(":/plugins/pcprofile/pcprofile.png")
        self.action = QAction(icon, 'Profile', self.iface.mainWindow())
        self.action.triggered.connect(self.profile)
        self.iface.addToolBarIcon(self.action)

        self.dock = SelectDock()
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

        self.iface.currentLayerChanged.connect(self.update_visibility)
        self.update_visibility()

        self.chart = Chart(self.iface.mapCanvas())
        self.view = View(self.iface, self.chart)
        self.tool = ProfileMapTool(self.iface, self.chart)

    def update_visibility(self):
        enable = False
        if self.iface.activeLayer():
            uri = self.iface.activeLayer().dataProvider().dataSourceUri()
            if "(pa)" in uri:
                enable = True
        self.action.setEnabled(enable)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

        self.iface.removeDockWidget(self.dock)

    def profile(self):
        self.iface.mapCanvas().setMapTool(self.tool)
        self.dock.show()
        self.view.show()
