#-*- coding:utf-8 -*-

"""
This file is part of data_repository.

data_repository is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

data_repository is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with data_repository.  If not, see <http://www.gnu.org/licenses/>.
"""

import __future__
import sys
from exparser.TangoPalette import *
from matplotlib import pyplot as plt

# Determine the experiment
for a in sys.argv:
	if 'exp1' in a:
		exp = a

# We use the baseline period, locked to the baseline end, as the baseline/
baseline = 'baseline'
baselineLock = 'end'

# Y axis boundaries for plots
yMin = 0.45
yMax = 1.35

# The number of pixels per degree for the current set-up
pxPerDeg = 34

# Number of subjects
N = 8

# Changing the trace lengths requires redoing the statistics
preTraceLen = 300
postTraceLen = 2000
preShowLen = 175
postShowLen = 1000
prepWin = 220

# Some styling for the plots
brightColor = orange[1]
darkColor = gray[5]
constColor = green[2]
swapColor = red[2]
onsetColor = blue[2]
color1 = blue[1]
color2 = orange[1]
flipSColor = brown[1]
flipEColor = brown[1]

brightStyle = '-'
darkStyle = '--'
constStyle = '-'
swapStyle = ':'
onsetStyle = '--'
flipSStyle = ':'
flipEStyle = ':'

plt.rc('font', family='Arial', size=10)

bigWide = 8,3
big = 4,6
norm = 4, 4
flat = 4, 2
