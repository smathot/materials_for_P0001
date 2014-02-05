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
import numpy as np
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from matplotlib import pyplot as plt

if 'exp1' in sys.argv:
	exp = 'exp1'
else:
	exp = 'exp2'

class MyReader(EyelinkAscFolderReader):
	
	saccSizeThr = 60
	
	def parseFile(self, path):
		
		self.trialId = -1
		return EyelinkAscFolderReader.parseFile(self, path)

	def startTrial(self, l):

		if len(l) > 2 and l[0] == 'MSG' and l[2] == 'start_trial':
			self.trialId += 1
			return self.trialId
		return None

	def initTrial(self, trialDict):
	
		sys.stdout.write('.')
		sys.stdout.flush()
		self.allowSacc = False
		trialDict['saccErr'] = 0
		
	def finishTrial(self, trialDict):
		
		self.flipSDelay = self.postSaccTime - self.saccSTime
		self.flipEDelay = self.postSaccTime - self.saccETime		
		self.saccDur = self.saccETime - self.saccSTime
		trialDict['flipSDelay'] = self.flipSDelay
		trialDict['flipEDelay'] = self.flipEDelay
		trialDict['saccDur'] = self.saccDur
		#print '%s\t%s\t%s' % (self.flipSDelay, self.flipEDelay, self.saccDur)
	
	def parseLine(self, trialDict, l):
		
		# Check for saccades after the cue
		if 'phase' in l and 'cue' in l:
			self.allowSacc = True
			self.cueTime = l[1]
			
		if 'phase' in l and 'postSacc' in l:
			self.postSaccTime = l[1]
			
		if self.tracePhase != None:
			# Only check for saccades larger than a specific threshold
			s = self.toSaccade(l)
			if s != None and s['size'] > self.saccSizeThr:
				# Check the first valid saccade
				if self.allowSacc:
					self.allowSacc = False
					self.saccSTime = s['sTime']
					self.saccETime = s['eTime']
					trialDict['saccLat2'] = self.saccSTime - self.cueTime
					trialDict['saccEndX'] = s['ex']
					trialDict['saccEndY'] = s['ey']
					trialDict['saccStartX'] = s['sx']
					trialDict['saccStartY'] = s['sy']
				# If a saccade was made during the baseline, set an error
				elif self.tracePhase == 'baseline':
					trialDict['saccErr'] = 1
					print 'Error! (Trial %d)' % trialDict['trialId']
				# Otherwise just stop collecting data after an eye movement.
				else:
					self.tracePhase = None

dm = MyReader(path='data/%s' % exp, maxN=20, maxTrialId=None, \
	blinkReconstruct=True, traceFolder='traces/%s' % exp, \
	only=None).dataMatrix()
dm.save('data/data.%s.npy' % exp)
