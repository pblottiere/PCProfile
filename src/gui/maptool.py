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

from threading import Thread

from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import QObject, pyqtSignal

from qgis.core import (QgsWkbTypes,
                       QgsPointXY,
                       QgsRectangle,
                       Qgis,
                       QgsMessageLog,
                       QgsDataSourceUri)
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool

from PCProfile.src.core import Database


class PointsFetcher(QObject, Thread):

    update = pyqtSignal()

    def __init__(self, uri, wkt, start_point, end_point, chart):
        super(QObject, self).__init__()
        super(Thread, self).__init__()
        self.uri = uri
        self.wkt = wkt
        self.chart = chart
        self.start_point = start_point
        self.end_point = end_point

    def run(self):
        db = Database(self.uri)
        db.open()
        points, xmin, xmax, zmin, zmax, pcids \
            = db.intersects_points(self.start_point, self.end_point, self.wkt)
        db.close()

        self.chart.update(points, xmin, xmax, zmin, zmax)

        self.update.emit()


class ProfileMapTool(QgsMapToolEmitPoint):

    fetching = pyqtSignal()
    fetched = pyqtSignal()

    def __init__(self, iface, chart):
        self.fetcher = None
        self.iface = iface
        self.chart = chart
        self._debug = False
        self.broke_size = 3.0
        QgsMapToolEmitPoint.__init__(self, self.iface.mapCanvas())
        self.rubberBand = QgsRubberBand(self.iface.mapCanvas(), True)
        self.rubberBand.setColor(QColor(255, 0, 0, 100))
        self.rubberBand.setWidth(2)

        self.rubberBand2 = QgsRubberBand(self.iface.mapCanvas(), True)
        self.rubberBand2.setColor(QColor(255, 0, 0, 50))

        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(True)
        self.rubberBand2.reset(True)

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False

        if not self.rectangle() or self.fetcher:
            return

        provider = self.iface.activeLayer().dataProvider()
        uri = QgsDataSourceUri(provider.dataSourceUri())

        polygon = self.rubberBand2.asGeometry()
        wkt = "SRID=32616;{}".format(polygon.asWkt())

        self.fetcher = PointsFetcher(uri, wkt, self.startPoint, self.endPoint, self.chart)
        self.fetcher.update.connect(self.update)
        self.fetcher.start()
        self.fetching.emit()

    def update(self):
        self.fetcher = None
        self.fetched.emit()

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def parallel(self, start, end, delta):
        x1,y1 = QgsPointXY(start)
        x2,y2 = QgsPointXY(end)
        length = start.distance(end)

        x1p = x1 + delta * ((y2-y1) / length)
        x2p = x2 + delta * ((y2-y1) / length)
        y1p = y1 + delta * ((x1-x2) / length)
        y2p = y2 + delta * ((x1-x2) / length)

        return QgsPointXY(x1p,y1p), QgsPointXY(x2p,y2p)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QgsWkbTypes.LineGeometry)
        self.rubberBand2.reset(QgsWkbTypes.PolygonGeometry)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return

        # rectangle
        start2, end2 = self.parallel(startPoint, endPoint, self.broke_size/2)
        start3, end3 = self.parallel(startPoint, endPoint, -self.broke_size/2)

        point1 = QgsPointXY(start2.x(), start2.y())
        point2 = QgsPointXY(end2.x(), end2.y())
        point3 = QgsPointXY(start3.x(), start3.y())
        point4 = QgsPointXY(end3.x(), end3.y())

        self.rubberBand2.addPoint(point1, False)
        self.rubberBand2.addPoint(point2, False)
        self.rubberBand2.addPoint(point4, False)
        self.rubberBand2.addPoint(point3, True) # true to update canvas
        self.rubberBand2.show()

        self.start_point_rect = point1
        self.end_point_rect = point4

        # center line
        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(startPoint.x(), endPoint.y())
        point3 = QgsPointXY(endPoint.x(), endPoint.y())
        point4 = QgsPointXY(endPoint.x(), startPoint.y())
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point3, True)
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None

        return QgsRectangle(self.start_point_rect, self.end_point_rect)

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()
