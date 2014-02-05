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
from analysis import helpers

for a in sys.argv:
	if 'exp1' in a:
		exp = a
		
if 'exp1.antiBias' in sys.argv and 'matchBias' not in sys.argv:
	raise Exception('Don\'t forget to enable matchBias for exp1.antiBias!')

if '-' not in sys.argv and 'checkMissing' not in sys.argv:
	raise Exception('Don\'t forget to enable checkMissing!')
		
print 'Session %s' % exp

if 'exp1' in exp:	
	print 'Reading exp1 data ...'
	dm = DataMatrix('data/data.exp1.npy')
else:
	print 'Reading exp2 data ...'
	dm = DataMatrix('data/data.exp2.npy')
print 'Done'

dm = dm.select('saccErr == 0')
dm = dm.select('saccLat2 != ""')
dm = dm.select('saccLat2 > 50')
dm = dm.select('saccLat2 < 2000')
dm = dm.select('flipSDelay > 0')
dm = dm.select('flipEDelay < 0')
dm = dm.select('saccDur < 100')

# Add the normalized saccade end position
dm = dm.addField('saccNormX', dtype=float)
dm['saccNormX'] = dm['saccEndX']
dm['saccNormX'][dm.where('saccSide == "right"')] = 1024 - \
	dm['saccEndX'][dm.where('saccSide == "right"')]
dm = dm.select('saccNormX < 342')

print 'From saccade onset: %.4f ms (%.4f)' % (dm['flipSDelay'].mean(), \
	dm['flipSDelay'].std())
print 'From saccade offset: %.4f ms (%.4f)' % (dm['flipEDelay'].mean(), \
	dm['flipEDelay'].std())
print 'Saccade duration: %.4f ms (%.4f)' % (dm['saccDur'].mean(), \
	dm['saccDur'].std())

for func in sys.argv:
	if hasattr(helpers, func):
		print 'Calling %s()' % func
		retVal = getattr(helpers, func)(dm)
		if retVal != None:
			dm = retVal
