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
__date__ = "2020/05/04"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"


import enum
from PyQt5 import QtGui
from qgis.core import QgsSettings


class Settings(object):


    class Snapshot(object):

        def __init__(self):
            setting = Settings.Chart.BackgroundColor
            name = Settings.get(setting, QtGui.QColor("white").name())
            self.background_color = name

            setting = Settings.Chart.AxisColor
            name = Settings.get(setting, QtGui.QColor("grey").name())
            self.axes_color = name

    class Chart(enum.Enum):

        BackgroundColor = "chart/background_color"
        AxisColor = "chart/axis_color"

    def get(setting, default, type=str):
        key = "pcprofile/{}".format(setting.value)
        value = QgsSettings().value(key, default)

        if type==bool:
            if str(value) == "true" or str(value) == "True":
                value = True
            else:
                value = False
        if type==int:
            value = int(value)

        return value

    def set(setting, value):
        key = "pcprofile/{}".format(setting.value)
        QgsSettings().setValue(key, value)
