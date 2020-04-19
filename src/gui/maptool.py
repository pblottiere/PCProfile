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

TABLE="terrain"
# SRID=32620
SRID=32616

class ProfileMapTool(QgsMapToolEmitPoint):
    updated = pyqtSignal()
    fake = pyqtSignal()

    def __init__(self, canvas, iface):
        self.iface = iface
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, True)
        self.rubberBand.setColor(QColor(255, 0, 0, 100))
        self.rubberBand.setWidth(1)
        self.reset()

        self._points_x = {}
        self._points_y = {}

        self._xmin = 0
        self._xmax = 10
        self._zmin = 0
        self._zmax = 10

        dir_path = os.path.dirname(os.path.realpath(__file__))
        qml = os.path.join(dir_path, "qml", "scatterplot.qml")
        self.view = QQuickView()
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.rootContext().setContextProperty("pyscatter", self)
        self.view.setColor(QColor("#404040"))
        self.view.setSource(QUrl.fromLocalFile(qml))

        self.container = QWidget.createWindowContainer(self.view)
        self.widget = QDockWidget()
        self.widget.setWidget(self.container)
        self.widget.setMinimumHeight(300)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.widget)

    @pyqtProperty(float, notify=fake)
    def xmin(self):
        # return self._xmin
        return self.iface.mapCanvas().extent().xMinimum()

    @pyqtProperty(float, notify=fake)
    def xmax(self):
        print(self._xmax)
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
        r = self.rectangle()
        if r is not None:
            print("Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum())

        layer = QgsProject.instance().mapLayersByName('hytech')[0]
        uri = QgsDataSourceUri(layer.dataProvider().dataSourceUri())
        db = QSqlDatabase.addDatabase("QPSQL", "myname");
        db.setHostName(uri.host())
        db.setDatabaseName(uri.database())
        db.setPort(int(uri.port()))
        db.setUserName(uri.username())
        db.setPassword(uri.password())
        db.open()

        q = "SELECT PC_Summary(pa) FROM {} LIMIT 1".format(TABLE)
        query = QSqlQuery(db)
        query.prepare(q)
        query.exec_()
        query.next()
        summary = query.record().value(0)
        summary = json.loads(summary)

        dims = summary["dims"]
        xindex = None
        yindex = None
        zindex = None
        index = 0
        for dim in dims:
            if dim["name"] == "X":
                xindex = index
            elif dim["name"] == "Y":
                yindex = index
            elif dim["name"] == "Z":
                zindex = index
            index += 1

        wkt = "SRID={};{}".format(SRID, r.asWktPolygon())
        q = "select id from {} where pc_intersects('{}'::geometry, pa)".format(TABLE, wkt)
        query = QSqlQuery(db)
        query.prepare(q)
        query.exec_()

        zvalues = []
        xvalues = []

        self._xmin = None
        self._xmax = None
        self._zmin = None
        self._zmax = None

        while query.next():
            record = query.record()
            pcid = record.value("id")
            q = "select pc_get(pc_explode(pc_intersection(pa, '{}'::geometry))) from {} where id = {}".format(wkt, TABLE, pcid)

            query2 = QSqlQuery(db)
            query2.prepare(q)
            query2.exec_()

            while query2.next():
                val = query2.record().value(0)
                val = val.replace('{', '').replace('}', '').split(',')

                x = float(val[xindex])
                z = float(val[zindex])

                if not self._xmin or x < self._xmin:
                    self._xmin = x

                if not self._xmax or x > self._xmax:
                    self._xmax = x

                if not self._zmin or z < self._zmin:
                    self._zmin = z

                if not self._zmax or z > self._zmax:
                    self._zmax = z

                zvalues.append(z)
                xvalues.append(x)

        db.close()
        del db
        QSqlDatabase.removeDatabase( "myname" )

        total = len(xvalues)
        step = 1
        treshold = 100000
        if total > treshold:
            perc = 100*treshold/total
            n = perc*total/100
            step =int(total / n)

        self._points_x = {}
        step_i = 0
        for i, x in enumerate(xvalues):
            if step_i == 0:
                self._points_x[str(i)] = x
                self._points_y[str(i)] = zvalues[i]

            step_i += 1
            if step_i == step:
                step_i = 0

        self.updated.emit()

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
