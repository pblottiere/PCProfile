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

from qgis.PyQt.QtGui import QColor

from qgis.core import (QgsWkbTypes,
                       QgsPointXY,
                       QgsRectangle,
                       Qgis,
                       QgsMessageLog,
                       QgsDataSourceUri)
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool

from PCProfile.src.core import Database

# from qgis.core import Qgis, QgsWkbTypes, QgsPointXY, QgsRectangle, QgsMessageLog, QgsDataSourceUri, QgsProject
# from qgis.PyQt.QtCore import Qt, QUrl, pyqtProperty, pyqtSignal, pyqtSlot
# from qgis.PyQt.QtGui import QColor
# from qgis.PyQt.QtSql import *
# from PyQt5.QtQuick import QQuickView
# from qgis.PyQt.QtWidgets import QWidget, QDockWidget
# import json


class ProfileMapTool(QgsMapToolEmitPoint):

    def __init__(self, iface, chart):
        self.iface = iface
        self.chart = chart
        QgsMapToolEmitPoint.__init__(self, self.iface.mapCanvas())
        self.rubberBand = QgsRubberBand(self.iface.mapCanvas(), True)
        self.rubberBand.setColor(QColor(255, 0, 0, 100))
        self.rubberBand.setWidth(1)
        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(True)

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        if not self.rectangle():
            return

        provider = self.iface.activeLayer().dataProvider()
        uri = QgsDataSourceUri(provider.dataSourceUri())
        db = Database(uri)
        db.open()
        wkt = "SRID=32616;{}".format(self.rectangle().asWktPolygon())
        points, xmin, xmax, zmin, zmax = db.intersects_points(wkt)
        db.close()

        self.chart.update(points, xmin, xmax, zmin, zmax)

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return
        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(startPoint.x(), endPoint.y())
        point3 = QgsPointXY(endPoint.x(), endPoint.y())
        point4 = QgsPointXY(endPoint.x(), startPoint.y())
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True) # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None

        return QgsRectangle(self.startPoint, self.endPoint)

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()
