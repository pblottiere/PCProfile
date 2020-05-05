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
from qgis.core import Qgis, QgsWkbTypes, QgsPointXY, QgsRectangle, QgsMessageLog, QgsDataSourceUri, QgsProject, QgsMessageLog, QgsGeometryUtils, QgsPoint
from qgis.PyQt.QtCore import Qt, QUrl, pyqtProperty, pyqtSignal, pyqtSlot
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtSql import *
from PyQt5.QtQuick import QQuickView
from qgis.PyQt.QtWidgets import QWidget, QDockWidget
import json


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

class Database(object):

    def __init__(self, uri):
        self.uri = uri
        self.name = "pcprofile"

    def open(self):
        self.db = QSqlDatabase.addDatabase("QPSQL", self.name);
        self.db.setHostName(self.uri.host())
        self.db.setDatabaseName(self.uri.database())
        self.db.setPort(int(self.uri.port()))
        self.db.setUserName(self.uri.username())
        self.db.setPassword(self.uri.password())
        self.db.open()

    def close(self):
        self.db.close()
        del self.db
        QSqlDatabase.removeDatabase(self.name)

    def dimensions(self):
        table = self.uri.table()
        q = "SELECT PC_Summary(pa) FROM {} LIMIT 1".format(table)
        query = QSqlQuery(self.db)
        query.prepare(q)
        query.exec_()
        query.next()
        summary = query.record().value(0)
        return json.loads(summary)["dims"]

    def dimension_index(self, name):
        for index, dim in enumerate(self.dimensions()):
            if dim["name"].lower() == name.lower():
                return index
        return None

    def intersects_patchs_id(self, wkt):
        table = self.uri.table()
        q = "select id from {} where pc_intersects('{}'::geometry, pa)".format(table, wkt)
        query = QSqlQuery(self.db)
        query.prepare(q)
        query.exec_()

        pcids = []
        while query.next():
            record = query.record()
            pcids.append(record.value("id"))

        return pcids

    def intersects_points(self, start, end, wkt):
        table = self.uri.table()
        points = []
        xmin = None
        xmax = None
        zmin = None
        zmax = None

        xindex = self.dimension_index("x")
        yindex = self.dimension_index("y")
        zindex = self.dimension_index("z")

        start_pt = QgsPoint()
        start_pt.setX(start.x())
        start_pt.setY(start.y())

        end_pt = QgsPoint()
        end_pt.setX(end.x())
        end_pt.setY(end.y())

        pcids = self.intersects_patchs_id(wkt)
        for pcid in pcids:
            q = "select pc_get(pc_explode(pc_intersection(pa, '{}'::geometry))) from {} where id = {}".format(wkt, table, pcid)

            query = QSqlQuery(self.db)
            query.prepare(q)
            query.exec_()

            while query.next():
                val = query.record().value(0)
                val = val.replace('{', '').replace('}', '').split(',')

                x = float(val[xindex])
                y = float(val[yindex])
                z = float(val[zindex])

                pt = QgsPoint()
                pt.setX(x)
                pt.setY(y)

                s = QgsGeometryUtils.perpendicularSegment(pt, start_pt, end_pt)
                p = s.pointN(-1)
                x = start.distance(QgsPointXY(p.x(), p.y()))

                if not xmin or x < xmin:
                    xmin = x

                if not xmax or x > xmax:
                    xmax = x

                if not zmin or z < zmin:
                    zmin = z

                if not zmax or z > zmax:
                    zmax = z

                points.append(Point(x, z))

        return points, xmin, xmax, zmin, zmax, pcids
