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
__copyright__ = "Copyright 2019, Paul Blottiere"
__date__ = "2019/07/19"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"


import os
from PyQt5 import QtWidgets, QtCore, uic, QtGui
from qgis.gui import QgsColorButton
from PCProfile.src.core import Settings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/settings.ui'))


class SettingsWidget(QtWidgets.QDialog, FORM_CLASS):

    updated = QtCore.pyqtSignal(Settings.Snapshot)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._background_color = QgsColorButton()
        self.mBackgroundLayout.addWidget(self._background_color)

        self._labels_color = QgsColorButton()
        self.mAxesLabelsLayout.addWidget(self._labels_color)

        self._axes_color = QgsColorButton()
        self.mAxesLayout.addWidget(self._axes_color)

        self._single_color = QgsColorButton()
        self.mSingleColorLayout.addWidget(self._single_color)

        self.mButtons.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.mButtons.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)

        self.read_settings()

    def read_settings(self):
        setting = Settings.Chart.BackgroundColor
        color = Settings.get(setting, QtGui.QColor("white"))
        self._background_color.setColor(QtGui.QColor(color))

        setting = Settings.Chart.AxisColor
        color = Settings.get(setting, QtGui.QColor("grey"))
        self._axes_color.setColor(QtGui.QColor(color))

        setting = Settings.Chart.LabelsColor
        color = Settings.get(setting, QtGui.QColor("red"))
        self._labels_color.setColor(QtGui.QColor(color))

    def cancel(self):
        snapshot = Settings.Snapshot()
        self.updated.emit(snapshot)
        self.read_settings()

    def apply(self):
        snapshot = Settings.Snapshot()
        snapshot.background_color = self._background_color.color().name()
        snapshot.axes_color = self._axes_color.color().name()
        snapshot.labels_color = self._labels_color.color().name()
        snapshot.opengl = self.opengl.isChecked()
        self.updated.emit(snapshot)

    def accept(self):
        self.store()
        self.apply()
        self.close()

    def store(self):
        color = self._background_color.color().name()
        setting = Settings.Chart.BackgroundColor
        Settings.set(setting, color)

        color = self._axes_color.color().name()
        setting = Settings.Chart.AxisColor
        Settings.set(setting, color)

        color = self._labels_color.color().name()
        setting = Settings.Chart.LabelsColor
        Settings.set(setting, color)

        value = self.opengl.isChecked()
        setting = Settings.Chart.OpenGL
        Settings.set(setting, value)
