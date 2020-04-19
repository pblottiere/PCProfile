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


class View(object):

    def __init__(self, iface, chart):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        qml = os.path.join(dir_path, "qml", "scatterplot.qml")
        self.view = QQuickView()
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)
        self.view.rootContext().setContextProperty("pychart", chart)
        self.view.setColor(QColor("#404040"))
        self.view.setSource(QUrl.fromLocalFile(qml))

        self.container = QWidget.createWindowContainer(self.view)
        self.widget = QDockWidget()
        self.widget.setWidget(self.container)
        self.widget.setMinimumHeight(300)
        iface.addDockWidget(Qt.BottomDockWidgetArea, self.widget)
