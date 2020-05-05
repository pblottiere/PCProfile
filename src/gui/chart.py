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
from qgis.PyQt.QtCore import Qt, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QObject
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtSql import *
from PyQt5.QtQuick import QQuickView
from qgis.PyQt.QtWidgets import QWidget, QDockWidget
import json

from PCProfile.src.core import Ramp, Settings


class Chart(QObject):
    updated = pyqtSignal()
    color = pyqtSignal()
    update_marker_size = pyqtSignal()
    update_settings = pyqtSignal()
    fake = pyqtSignal()

    def __init__(self, canvas):
        super().__init__()

        self.canvas = canvas
        self._points = []
        self._points_x = {}
        self._points_y = {}

        self._xmin = 0
        self._xmax = 10
        self._zmin = 0
        self._zmax = 10

        self._budget = 100000
        self._scaled = True
        self._marker_size = 2.0
        self._ramp = Ramp("elevation")

        self.read_settings()

    @pyqtSlot(str, result='QColor')
    def ramp_color(self, step):
        return self._ramp.values[int(step)]

    @pyqtProperty(float, notify=update_marker_size)
    def marker_size(self):
        return self._marker_size

    @pyqtProperty(bool, notify=fake)
    def is_scaled(self):
        return self._scaled

    @pyqtProperty(float, notify=fake)
    def xmin(self):
        return self._xmin

    @pyqtProperty(float, notify=fake)
    def xmax(self):
        return self._xmax

    @pyqtProperty(float, notify=fake)
    def zmax(self):
        return self._zmax + 1

    @pyqtProperty(float, notify=fake)
    def zmin(self):
        return self._zmin - 1

    @pyqtProperty('QVariantMap')
    def points_x(self):
        return self._points_x

    @pyqtProperty('QVariantMap')
    def points_y(self):
        return self._points_y

    @pyqtSlot(str)
    def log_from_qml(self, param):
        print(param)

    @pyqtProperty(QColor, notify=update_settings)
    def background_color(self):
        return QColor(self._settings.background_color)

    def read_settings(self, settings=None):
        if not settings:
            settings = Settings.Snapshot()
        self._settings = settings

        self.update_settings.emit()

    def set_scaled(self, status):
        self._scaled = status
        self.updated.emit()

    def set_budget(self, n):
        self._budget = n
        self.sample()
        self.updated.emit()

    def set_color(self, name):
        self._ramp = Ramp(name)
        self.color.emit()

    def set_marker_size(self, size):
        self._marker_size = size
        self.update_marker_size.emit()

    def sample(self):
        total = len(self._points)
        step = 1
        if total > self._budget:
            perc = 100*self._budget/total
            n = perc*total/100
            step = int(total / n)

        step_i = 0

        self._points_x = {}
        self._points_y = {}
        for i, point in enumerate(self._points):
            if step_i == 0:
                self._points_x[str(i)] = point.x
                self._points_y[str(i)] = point.y

            step_i += 1
            if step_i == step:
                step_i = 0

    def update(self, points, xmin, xmax, zmin, zmax):
        self._xmin = xmin
        self._xmax = xmax
        self._zmin = zmin
        self._zmax = zmax
        self._points = points
        self.sample()
        self.updated.emit()
