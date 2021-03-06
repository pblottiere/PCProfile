# -*- coding: utf-8 -*-

"""
QGIS Plugin for monitoring performances.

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


import os

from qgis.core import QgsProject
from qgis.PyQt import QtCore, QtWidgets, uic

from PCProfile.src.core import Settings


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/select.ui'))

class SelectDock(QtWidgets.QDockWidget, FORM_CLASS):

    def __init__(self, chart, maptool):
        super().__init__()
        self.chart = chart
        self.maptool = maptool
        self.setupUi(self)
        self.size.valueChanged.connect(self.marker_size)
        self.broke.valueChanged.connect(self.broke_size)
        self.render.currentIndexChanged.connect(self.render_color)
        self.scaled.stateChanged.connect(self.scaled_changed)
        self.budget.valueChanged.connect(self.budget_changed)

        self.block_signal = False
        self.read_settings()

    def read_settings(self, settings=None):
        if not settings:
            settings = Settings.Snapshot()

        # don't want to update chart when I modify default value in
        # settings window
        self.block_signal = True
        self.budget.setValue(settings.budget)
        self.block_signal = False

    def budget_changed(self):
        if not self.block_signal:
            self.chart.set_budget(self.budget.value())

    def scaled_changed(self):
        self.chart.set_scaled(self.scaled.isChecked())

    def render_color(self):
        self.chart.set_color(self.render.currentText())

    def marker_size(self):
        self.chart.set_marker_size(self.size.value())

    def broke_size(self):
        self.maptool.broke_size = self.broke.value()
