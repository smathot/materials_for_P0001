#!/usr/bin/env python
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

import sys
from exparser.DataMatrix import DataMatrix
from analysis import helpers, fitting
from exparser import Cache, Tools

exp = None
for a in sys.argv:
	if 'exp1' in a:
		exp = a
if exp == None:
	raise Exception('Please specify exp1 or exp1.antiBias')

if 'exp1.antiBias' in sys.argv and '@matchBias' not in sys.argv and \
	'@matchBias:redo' not in sys.argv:
	raise Exception('Don\'t forget to enable @matchBias for exp1.antiBias!')
if exp == 'exp1' and '@matchBias' in sys.argv:
	raise Exception('Don\'t enable @matchBias for exp1!')
if '-' not in sys.argv and '@checkMissing' not in sys.argv:
	raise Exception('Don\'t forget to enable @checkMissing!')

print 'Session %s' % exp

if 'exp1' in exp:
	print 'Reading exp1 data ...'
	dm = DataMatrix('data/data.exp1.npy')
else:
	print 'Reading exp2 data ...'
	dm = DataMatrix('data/data.exp2.npy')
print 'Done'

Tools.analysisLoop(dm, mods=[helpers, fitting], pre=['filter'],
	cachePrefix='autoCache.%s.' % exp)
