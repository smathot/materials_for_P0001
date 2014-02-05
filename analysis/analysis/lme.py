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

from exparser.rbridge import RBridge
 
def mixedModelTrace(dm, fixedEffects, randomEffects, winSize=1, nSim=1000, \
	effectIndex=0):

	"""
	This function has been copied from `exparser.TraceKit`, to deal with the
	peculiarities of this dataset, and the fact that no satisfactory general-
	purpose implementation exists yet.
	"""

	global R
	try:
		R
	except:
		R = RBridge()
		
	R.write('library("lme4")')
	R.write('library("languageR")')
		
	traceLen = traceParams['traceLen']		
	aPVal = np.zeros( (traceLen, 3) )
	for i in range(0, traceLen, winSize):
		# First calculate the mean value for the current signal slice for each
		# trial and save that in a copy of the DataMatrix. Also determine the
		# gaze bias for each sample.
		_dm = dm.addField('mmdv__', dtype=float)
		_dm = dm.addField('bias__', dtype=float)
		for trialId in range(len(_dm)):
			pupilTrace = getTrace(_dm[trialId], signal='pupil', **traceParams)
			xTrace = getTrace(_dm[trialId], signal='x', **traceParams)
			if i < len(aTrace):
				sliceMean = aTrace[i:i+winSize].mean()
			else:
				sliceMean = np.nan
			_dm['mmdv__'][trialId] = sliceMean
			
			
		# Do mixed effects
		__dm = _dm.selectColumns(fixedEffects+randomEffects+['mmdv__'])
		R.load(__dm)
		s = R.call('''data$subject_nr <- factor(data$subject_nr)
			mme = lmer(mmdv__ ~ %s + (1|subject_nr), data=data)
			sum = summary(mme)
			print(sum)
			pv = pvals.fnc(mme, nsim=100, ndigits=5)
			print(pv)
			p = pv$fixed$Pr[2]
			ciLow = pv$fixed$HPD95lower[2]
			ciHigh = pv$fixed$HPD95upper[2]
			cat(sprintf('START%%s,%%s,%%sEND\n', p, ciLow, ciHigh))
			''' % '+'.join(fixedEffects))
		s = s[s.find('START')+5:s.find('END')]
		l = s.split(',')
		pVal = float(l[0])
		ciLow = float(l[1])
		ciHigh = float(l[2])
		aPVal[i:i+winSize,0] = pVal
		aPVal[i:i+winSize,1] = ciLow
		aPVal[i:i+winSize,2] = ciHigh
		print '%.4d: p = %.3f (%f - %f)' % (i, pVal, ciHigh, ciLow)
				
	return aPVal
