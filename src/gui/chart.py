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


from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool
from qgis.core import Qgis, QgsWkbTypes, QgsPointXY, QgsRectangle, QgsMessageLog, QgsDataSourceUri, QgsProject
from qgis.PyQt.QtCore import Qt, QUrl, pyqtProperty, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtSql import *
from PyQt5.QtQuick import QQuickView
from qgis.PyQt.QtWidgets import QWidget, QDockWidget
import json


class Chart(QObject):
    updated = pyqtSignal()
    fake = pyqtSignal()

    def __init__(self):
        self._points_x = {}
        self._points_y = {}

        self._xmin = 0
        self._xmax = 10
        self._zmin = 0
        self._zmax = 10

    @pyqtProperty(float, notify=fake)
    def xmin(self):
        # return self._xmin
        return self.iface.mapCanvas().extent().xMinimum()

    @pyqtProperty(float, notify=fake)
    def xmax(self):
        return self.iface.mapCanvas().extent().xMaximum()
        # return self._xmax

    @pyqtProperty(float, notify=fake)
    def zmax(self):
        print(self._zmax)
        return self._zmax + 1

    @pyqtProperty(float, notify=fake)
    def zmin(self):
        print(self._zmin)
        return self._zmin - 1

    @pyqtProperty('QVariantMap')
    def points_x(self):
        return self._points_x

    @pyqtProperty('QVariantMap')
    def points_y(self):
        return self._points_y
