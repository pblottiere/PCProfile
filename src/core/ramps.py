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
__date__ = "2020/04/25"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"

import os

from qgis.PyQt.QtGui import QImage, QColor

from .settings import Settings


class Ramp(object):

    def __init__(self, name="elevation"):
        self.values = []
        self.name = name
        self._color = Settings.Snapshot().single_color
        self._generate()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c
        self._generate()

    def _generate(self):
        self.values = []
        n = 12
        if "single" in self.name.lower():
            for i in range(0, n):
                self.values.append(QColor(self._color))
        elif "elevation" in self.name.lower():
            path = os.path.dirname(os.path.realpath(__file__))
            ramp = os.path.join(path, "ramps", "dem.png")
            img = QImage(ramp)
            step = img.size().height() / n

            middle_x = img.size().width()/2
            for i in range(0, n):
                y = i*step
                self.values.append(img.pixelColor(middle_x, y))
            self.values.reverse()
