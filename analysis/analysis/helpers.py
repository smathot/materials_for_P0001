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
from matplotlib import pyplot as plt
from exparser import TraceKit, TangoPalette
from exparser.PivotMatrix import PivotMatrix
from exparser.DataMatrix import DataMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser.Cache import cachedDataMatrix
import numpy as np
from scipy.stats import ttest_rel, linregress
import shutil
import sys
from fitting import *
from const import *
from figure import *

@cachedDataMatrix
def filter(dm):

	"""
	Filters the DataMatrix.

	Arguments:
	dm		--	DataMatrix

	Returns:
	A filtered DataMatrix.
	"""

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
	return dm

def errorTrace(aStats, dm1, dm2, phase, signal='pupil'):

	"""
	Calculates minimum and maximum values for two traces, in order to plot a
	two-trace plot with 95% confidence intervals.

	Arguments:
	aStats		--	An array as returns by `TraceKit.mixedModelTrace()`.
	dm1			--	The first DataMatrix.
	dm2			--	The second DataMatrix.
	phase		--	The phase to analyze.

	Keyword arguments:
	signal		--	The signal to use for the error. (default='pupil')

	Returns:
	An (aErr1, aErr2, aDiff) tuple, where aErrX are two dimensional array with
	upper and lower bounds for the traces. aDiff corresponds to the difference
	traces.
	"""

	traceLen = aStats.shape[0]
	if phase == 'postSacc':
		lock = 'start'
	else:
		lock = 'end'
	# Get the two average traces
	a1 = TraceKit.getTraceAvg(dm1, signal=signal, phase=phase, lock=lock,
		traceLen=traceLen, baseline=baseline, baselineLock=baselineLock)
	a2 = TraceKit.getTraceAvg(dm2, signal=signal, phase=phase, lock=lock,
		traceLen=traceLen, baseline=baseline, baselineLock=baselineLock)
	# Get the differenceTrace
	aDiff = a1[1] - a2[1]
	minSlope = aStats[:,1]
	maxSlope = aStats[:,2]
	minErr = (aDiff-minSlope)/2
	maxErr = (maxSlope-aDiff)/2
	minErr = TraceKit.smooth(minErr, windowLen=31)
	maxErr = TraceKit.smooth(maxErr, windowLen=31)
	aErr1 = np.array([minErr, maxErr])
	aErr2 = np.array([maxErr, minErr])
	return aErr1, aErr2, aDiff

def runStats(dm):

	"""
	Runs the LMM on the traces.

	Arguments:
	dm		--	DataMatrix
	"""

	winSize = 1

	randomEffects = ['subject_nr']
	fixedEffects = ['saccSide']

	# ***
	# Horizontal position stats
	# ***
	# Select DataMatrices
	a = TraceKit.mixedModelTrace(dm, fixedEffects, \
		randomEffects, winSize=winSize, nSim=None, signal='x', \
		phase='cue', traceLen=preTraceLen, baseline=baseline, \
		baselineLock='end', lock='end')
	np.save('stats/%s/x.pre.npy' % exp, a)

	# ***
	# Pupil stats
	# ***
	# Also run the pre-saccade phase for the swap and constant together. To do
	# this we need to swap the lines for the pre-signal

	fixedEffects = ['saccCol', 'gazeBias']

	_dmSwap = dm.select('cond == "swap"')
	_dmConstant = dm.select('cond == "constant"')
	_dmSwap.recode('saccCol', [('white', 'black'), ('black', 'white')])
	a = lme.mixedModelTrace(_dmSwap + _dmConstant, fixedEffects, \
		randomEffects, winSize=winSize, nSim=None, signal='pupil', \
		phase='cue', traceLen=preTraceLen, baseline=baseline, \
		baselineLock='end', lock='end')
	np.save('stats/%s/swap.constant.pre.npy' % exp, a)
	# Now run all the separate phases
	for cond in ('swap', 'constant', 'onset'):
		_dm = dm.select('cond == "%s"' % cond)
		a = TraceKit.mixedModelTrace(_dm, fixedEffects, randomEffects,
			winSize=winSize, nSim=None, signal='pupil', phase='cue',
			traceLen=preTraceLen, baseline=baseline, lock='end',
			baselineLock=baselineLock)
		np.save('stats/%s/%s.pre.npy' % (exp, cond), a)
		a = TraceKit.mixedModelTrace(_dm, fixedEffects, randomEffects,
			winSize=winSize, nSim=None, signal='pupil', phase='postSacc',
			traceLen=postTraceLen, baseline=baseline, baselineLock=baselineLock)
		np.save('stats/%s/%s.post.npy' % (exp, cond), a)

def mainPlots(dm):

	"""
	Generates the main plots

	Arguments:
	dm		--	DataMatrix
	"""

	for subjectNr in ['all']: # + dm.unique('subject_nr'):
		print baseline, subjectNr
		if subjectNr == 'all':
			_dm = dm
		else:
			_dm = dm.select('subject_nr == %d' % subjectNr, verbose=False)

		fig = newFig(size=big)
		plt.subplots_adjust(wspace=0, hspace=0)

		# Pre difference plot
		ax = plt.subplot2grid((4,7), (0,0), colspan=1)
		plt.ylabel('Pupil-size diff (norm.)')
		plt.ylim(-.5, .2)
		ax.spines["right"].set_visible(False)
		ax.get_yaxis().tick_left()
		ax.axhline(0, linestyle='--', color='black')
		plt.xticks(range(150, preTraceLen+1, 150), range(-preTraceLen+150, \
			1, 150))
		plt.yticks([.0, -.2, -.4])
		#ax.get_xaxis().set_ticklabels([])
		plt.xlim(0, preTraceLen)
		# Draw saccade onsets
		sMin = _dm['flipSDelay'].min()
		sMax = _dm['flipSDelay'].max()
		sMean = _dm['flipSDelay'].mean()
		plt.axvspan(preTraceLen-sMin, preTraceLen-sMax, color=flipSColor, \
			alpha=.1)
		plt.axvline(preTraceLen-sMean, color=flipSColor, linestyle=flipEStyle)
		for cond in ('constant', 'swap', 'onset'):
			print '\t%s' % cond
			__dm = _dm.select('cond == "%s"' % cond, verbose=False)
			_dmWhite = __dm.select('saccCol == "white"', verbose=False)
			_dmBlack = __dm.select('saccCol == "black"', verbose=False)
			xPre, blackPre, err = TraceKit.getTraceAvg(_dmBlack, signal= \
				'pupil', phase='cue', lock='end', traceLen=preTraceLen, \
				baseline=baseline)
			xPre, whitePre, err = TraceKit.getTraceAvg(_dmWhite, signal= \
				'pupil', phase='cue', lock='end', traceLen=preTraceLen, \
				baseline=baseline)
			if cond == 'constant':
				col = constColor
				style = constStyle
			elif cond == 'swap':
				col = swapColor
				style = swapStyle
			else:
				col = onsetColor
				style = onsetStyle
			plt.plot(xPre, whitePre-blackPre, color=col, label=cond,
				linestyle=style)
			if cond == 'swap':
				plt.plot(xPre, blackPre-whitePre, ':', color=col, label= \
					'inverse swap')
		plt.xlim(preTraceLen-preShowLen, preTraceLen)

		# Post difference plot
		ax = plt.subplot2grid((4,7), (0,1), colspan=6)
		plt.ylim(-.5, .2)
		ax.spines["left"].set_visible(False)
		plt.axvline(0, linestyle='--', color='black')
		ax.axhline(0, linestyle='--', color='black')
		plt.xlim(0, postTraceLen)
		plt.xticks(range(150, postTraceLen, 150))
		#ax.get_yaxis().tick_right()
		ax.get_yaxis().set_ticklabels([])
		# Title
		plt.text(0.1, 0.9, 'Difference', horizontalalignment='center', \
			verticalalignment='center', transform=ax.transAxes)
		# Draw saccade offsets
		eMin = -_dm['flipEDelay'].min()
		eMax = -_dm['flipEDelay'].max()
		eMean = -_dm['flipEDelay'].mean()
		plt.axvspan(eMin, eMax, color=flipEColor, alpha=.1)
		plt.axvline(eMean, color=flipEColor, linestyle=flipEStyle)
		# Draw 'window of preparation'
		plt.axvspan(0, prepWin, color=green[1], alpha=.2)
		for cond in ('constant', 'swap', 'onset'):
			print '\t%s' % cond
			__dm = _dm.select('cond == "%s"' % cond, verbose=False)
			_dmWhite = __dm.select('saccCol == "white"', verbose=False)
			_dmBlack = __dm.select('saccCol == "black"', verbose=False)
			xPost, blackPost, err = TraceKit.getTraceAvg(_dmBlack, signal= \
				'pupil', phase='postSacc', lock='start', traceLen= \
				postTraceLen, baseline=baseline)
			xPost, whitePost, err = TraceKit.getTraceAvg(_dmWhite, signal= \
				'pupil', phase='postSacc', lock='start', traceLen= \
				postTraceLen, baseline=baseline)
			if cond == 'constant':
				col = constColor
				style = constStyle
			elif cond == 'swap':
				col = swapColor
				style = swapStyle
			else:
				col = onsetColor
				style = onsetStyle
			plt.plot(xPost, whitePost-blackPost, color=col, label=cond,
				linestyle=style)
			if cond == 'swap':
				plt.plot(xPost, blackPost-whitePost, ':', color=col, label= \
					'inverse swap')
		plt.xlim(0, postShowLen)
		plt.legend(frameon=False)

		# Main plots
		i = 1
		for cond in ('constant', 'swap', 'onset'):
			print '\t%s' % cond
			__dm = _dm.select('cond == "%s"' % cond, verbose=False)
			_dmWhite = __dm.select('saccCol == "white"', verbose=False)
			_dmBlack = __dm.select('saccCol == "black"', verbose=False)
			if subjectNr == 'all':
				# Load stats from disk (need to be calculated before by `runStats()`
				aStatsPre = np.load('stats/%s/%s.pre.npy' % (exp, cond))
			ax = plt.subplot2grid((4,7), (i,0), colspan=1)
			ax.spines["right"].set_visible(False)
			ax.get_yaxis().tick_left()
			ax.axhline(1.0, linestyle='--', color='black')
			# Draw saccade onsets
			sMin = __dm['flipSDelay'].min()
			sMax = __dm['flipSDelay'].max()
			sMean = __dm['flipSDelay'].mean()
			plt.axvspan(preTraceLen-sMin, preTraceLen-sMax, color=flipSColor, \
				alpha=.1)
			plt.axvline(preTraceLen-sMean, color=flipSColor,
			   linestyle=flipSStyle)

			if subjectNr == 'all':
				TraceKit.markStats(ax, aStatsPre[:,0], minSmp=200, alpha=.01)
				aErrWhite, aErrBlack, aDiff = errorTrace(aStatsPre, _dmWhite,
					_dmBlack, phase='cue')
			else:
				aErrWhite, aErrBlack, aDiff = None, None, None
			plt.ylim(yMin, yMax)
			TraceKit.plotTraceAvg(ax, _dmWhite, aErr=aErrWhite, signal='pupil',
				phase='cue', lock='end', traceLen=preTraceLen,
				baseline=baseline, baselineLock=baselineLock,
				lineColor=brightColor, errColor=brightColor,
				lineStyle=brightStyle)
			TraceKit.plotTraceAvg(ax, _dmBlack, aErr=aErrBlack, signal='pupil',
				phase='cue', lock='end', traceLen=preTraceLen,
				baseline=baseline, baselineLock=baselineLock,
				lineColor=darkColor, errColor=darkColor, lineStyle=darkStyle)
			plt.xticks(range(150, preTraceLen+1, 150), range(-preTraceLen+150, \
				1, 150))
			if i < 3:
				ax.get_xaxis().set_ticklabels([])
			if cond == 'swap':
				plt.ylabel('Pupil size (norm.)')
			#plt.xlim(0, preTraceLen)
			plt.xlim(preTraceLen-preShowLen, preTraceLen)

			# Post-saccade
			ax = plt.subplot2grid((4,7), (i,1), colspan=6)
			ax.spines["left"].set_visible(False)
			plt.axvline(0, linestyle='--', color='black')
			ax.axhline(1.0, linestyle='--', color='black')
			# Title
			plt.text(0.1, 0.9, cond, horizontalalignment='center', \
				verticalalignment='center', transform=ax.transAxes)
			# Draw saccade offsets
			eMin = -__dm['flipEDelay'].min()
			eMax = -__dm['flipEDelay'].max()
			eMean = -__dm['flipEDelay'].mean()
			plt.axvspan(eMin, eMax, color=flipEColor, \
				alpha=.1)
			plt.axvline(eMean, color=flipEColor, linestyle=flipEStyle)

			if subjectNr == 'all':
				aStatsPost = np.load('stats/%s/%s.post.npy' % (exp, cond))
				TraceKit.markStats(ax, aStatsPost[:,0], minSmp=200, alpha=.4)
				aErrWhite, aErrBlack, aDiff = errorTrace(aStatsPost, _dmWhite,
					_dmBlack, phase='postSacc')
			else:
				aErrWhite, aErrBlack, aDiff = None, None, None
			plt.ylim(yMin, yMax)
			TraceKit.plotTraceAvg(ax, _dmWhite, aErr=aErrWhite, signal='pupil',
				phase='postSacc', traceLen=postTraceLen, baseline=baseline,
				lineColor=brightColor, errColor=brightColor, \
				baselineLock=baselineLock, label='Bright',
				lineStyle=brightStyle)
			TraceKit.plotTraceAvg(ax, _dmBlack, aErr=aErrBlack, signal='pupil',
				phase='postSacc', traceLen=postTraceLen, baseline=baseline,
				lineColor=darkColor, errColor=darkColor, \
				baselineLock=baselineLock, label='Dark', lineStyle=darkStyle)
			plt.xlim(0,postTraceLen)
			if i == 3:
				plt.xlabel('Time after saccade (ms)')
			if i < 3:
				ax.get_xaxis().set_ticklabels([])
			plt.xticks(range(150, postTraceLen, 150))
			ax.get_yaxis().tick_right()
			ax.get_yaxis().set_ticklabels([])

			if cond == 'constant':
				plt.legend(frameon=False, loc='lower left')
			plt.xlim(0, postShowLen)
			i += 1

		saveFig('main.subject.%s' % subjectNr, show=False)

def posTracePlots(dm, signal='x'):

	"""
	Analyzes the position traces. Most useful to see whether the eyes gravitate
	towards the saccade side before the actual saccade.

	Arguments:
	dm		--	DataMatrix

	Keyword arguments:
	signal	--	Indicates the trace signal. (default='x')
	"""

	for subjectNr in ['all'] + dm.unique('subject_nr'):
		print baseline, subjectNr
		if subjectNr == 'all':
			_dm = dm
		else:
			_dm = dm.select('subject_nr == %d' % subjectNr, verbose=False)

		fig = newFig(size=(12,4))
		plt.subplots_adjust(wspace=0)
		# Select DataMatrices
		_dmLeft= _dm.select('saccSide == "left"', verbose=False)
		_dmRight = _dm.select('saccSide == "right"', verbose=False)
		# Get stats
		if subjectNr == 'all':
			aStatsPre = np.load('stats/%s/x.pre.npy' % exp)
			print 'First significant: %s' % np.where(aStatsPre[:,0] < .05)[0]
			aErrLeft, aErrRight, aDiff = errorTrace(aStatsPre, _dmLeft, _dmRight, \
				phase='cue', signal='x')
		else:
			aErrLeft, aErrRight, aDiff = None, None, None
		# Pre-saccade
		ax = plt.subplot2grid((1,7), (0,0), colspan=1)
		plt.axhline(384, linestyle='--', color='black')
		plt.ylim(0, 1024)
		plt.xlim(0, preTraceLen)
		plt.xticks(range(0, preTraceLen, 50), range(-preTraceLen, 1, 50))

		if subjectNr == 'all':
			TraceKit.markStats(ax, aStatsPre[:,0], minSmp=1)
		TraceKit.plotTraceAvg(ax, _dmLeft, signal=signal, aErr=aErrLeft, \
			phase='cue', lock='end', traceLen=preTraceLen,
			lineColor=brightColor, errColor=brightColor)
		TraceKit.plotTraceAvg(ax, _dmRight, signal=signal, aErr=aErrRight, \
			phase='cue', lock='end', traceLen=preTraceLen,
			lineColor=darkColor, errColor=darkColor)

		# Post-saccade
		ax = plt.subplot2grid((1,7), (0,1), colspan=6)
		plt.axhline(384, linestyle='--', color='black')
		plt.ylim(0, 1024)
		plt.xlim(0, postTraceLen)
		plt.xticks(range(0, postTraceLen, 50))
		plt.yticks([])

		TraceKit.plotTraceAvg(ax, _dmLeft, signal=signal,
			phase='postSacc', traceLen=postTraceLen,
			lineColor=brightColor, errColor=brightColor)
		TraceKit.plotTraceAvg(ax, _dmRight, signal=signal,
			phase='postSacc', traceLen=postTraceLen,
			lineColor=darkColor, errColor=darkColor)
		saveFig('%s.posTrace.%s' % (signal, subjectNr), show=True)

def saccMetrics(dm):

	"""
	Analyzes and plots the saccade latency, duration, etc.

	Arguments:
	dm		--	DataMatrix
	"""

	newFig()
	print dm['saccLat2'].dtype
	plt.subplot(2,1,1)
	plt.hist(dm['saccLat'], bins=100, histtype='step', color=color1,
		label='online')
	plt.hist(dm['saccLat2'], bins=100, histtype='step', color=color2,
		label='offline')
	plt.legend()
	plt.subplot(2,1,2)
	plt.hist(dm['saccDur'], bins=100, histtype='step', color=color1,
		label='offline')
	print 'Saccade latency online: M = %.2f, SD = %.2f' % \
		(dm['saccLat'].mean(), dm['saccLat'].std())
	print 'Saccade latency offline: M = %.2f, SD = %.2f' % \
		(dm['saccLat2'].mean(), dm['saccLat2'].std())
	saveFig('saccMetrics')

def saccEndPoints(dm):

	"""
	Analyzes and plots the saccade endpoints.

	Arguments:
	dm		--	DataMatrix
	"""

	i = 1
	newFig()
	l = [['Condition', 'Luminance', 'SaccDir', 'End X (M)', 'End X (SD)']]
	for cond in ('constant', 'swap', 'onset'):
		for saccCol in ('white', 'black'):
			_dm = dm.select('cond == "%s"' % cond).select('saccCol == "%s"' \
				% saccCol)
			a = (_dm.select('saccSide == "left"')['saccEndX'] - 512) / pxPerDeg
			l.append([cond, saccCol, 'left', a.mean(), a.std()])
			a = (_dm.select('saccSide == "right"')['saccEndX'] - 512) / pxPerDeg
			l.append([cond, saccCol, 'right', a.mean(), a.std()])
			plt.subplot(3,2,i)
			plt.xlim(0,1024)
			plt.ylim(0,768)
			plt.title('%s - %s' % (cond, saccCol))
			plt.axvline(1024/2, linestyle=':', color='black')
			plt.axvline(1024/6, linestyle=':', color='black')
			plt.axvline(1024-1024/6, linestyle=':', color='black')
			plt.axhline(768/2, linestyle=':', color='black')
			plt.plot(_dm['saccEndX'], _dm['saccEndY'], ',', color=darkColor)
			if cond != 'onset':
				plt.xticks([])
			else:
				plt.xticks([0,512,1024])
			if saccCol != 'white':
				plt.yticks([])
			else:
				plt.yticks([0,384,768])
			i += 1
	dm = DataMatrix(l)
	dm.sort(['SaccDir'])
	dm.save('output/%s/saccEndPoints.csv' % exp)
	print dm
	saveFig('endPoints', show=True)

def descriptives(dm):

	"""Prints descriptive statistics and perform some basic anovas."""


	pm = PivotMatrix(dm, ['cond'], ['subject_nr'], dv='saccEndX', func='size')
	pm.save('output/%s/cellCount.cond.csv' % exp)
	print pm

	quit()

	pm = PivotMatrix(dm, ['saccSide'], ['subject_nr'], dv='saccEndX')
	pm.save('output/%s/saccEndX.saccSide.csv' % exp)

	pm = PivotMatrix(dm, ['saccSide'], ['subject_nr'], dv='saccNormX')
	pm.save('output/%s/saccNormX.saccSide.csv' % exp)

	pm = PivotMatrix(dm, ['cond', 'saccSide'], ['subject_nr'], dv='saccLat2')
	pm.save('output/%s/saccLat.cond.saccSide.csv' % exp)

	pm = PivotMatrix(dm, ['saccCol'], ['subject_nr'], dv='saccLat2')
	pm.save('output/%s/saccLat.saccCol.csv' % exp)

	pm = PivotMatrix(dm, ['cond'], ['subject_nr'], dv='saccLat2')
	pm.save('output/%s/saccLat.cond.csv' % exp)

	aov = AnovaMatrix(dm, ['cond'], 'saccLat2', subject='subject_nr')
	aov.save('output/%s/aov.cond.saccLat.csv' % exp)

	print 'Saccade latency: %.4f (%.4f)' % (dm['saccLat2'].mean(), \
		dm['saccLat2'].std())

@cachedDataMatrix
def matchBias(dm):

	"""
	Matches trials based on a bias towards the saccade target side.

	Arguments:
	dm		--	DataMatrix

	Returns:
	A matched DataMatrix.
	"""

	dm = dm.addField('gazeBias', dtype=float)
	print 'Adding gaze-bias information ...'
	for i in dm.range():
		a = TraceKit.getTrace(dm[i], signal='x', phase='cue', \
			traceLen=preTraceLen, lock='end', nanPad=False)
		saccSide = dm['saccSide'][i]
		_a = a[:-50]
		bias = (_a-512).mean()
		if saccSide == 'left':
			bias *= -1
		dm['gazeBias'][i] = bias
	print 'All: M = %.4f, SD = %.4f' % (dm['gazeBias'].mean(), \
		dm['gazeBias'].std())
	newFig()
	plt.subplot(2,1,1)
	plt.title('Unbalanced: M = %.4f, SD = %.4f' % (dm['gazeBias'].mean(), \
		dm['gazeBias'].std()))
	plt.hist(dm['gazeBias'], bins=50, color=blue[1])
	plt.axvline(dm['gazeBias'].mean())
	#dm = dm.select('gazeBias < 0')
	dm = dm.balance('gazeBias', .1, verbose=True)
	#newDm = None
	#for _dm in dm.group('subject_nr'):
		#print 'Balancing subject_nr %d' % _dm['subject_nr'][0]
		#if newDm == None:
			#newDm = _dm.balance('gazeBias', 1)
		#else:
			#newDm += _dm.balance('gazeBias', 1)
	#dm = newDm
	dm = dm.select('__unbalanced__ == 0')
	plt.subplot(2,1,2)
	plt.title('Balanced: M = %.4f, SD = %.4f' % (dm['gazeBias'].mean(), \
		dm['gazeBias'].std()))
	plt.hist(dm['gazeBias'], bins=50, color=blue[1])
	plt.axvline(dm['gazeBias'].mean())
	print 'Antibias: M = %.4f, SD = %.4f' % (dm['gazeBias'].mean(), \
		dm['gazeBias'].std())
	saveFig('gazeBias')
	return dm

@cachedDataMatrix
def checkMissing(dm, checkCue=True, checkPostSacc=True):

	"""
	Checks whether there is missing data in the pupil traces, and filters trials
	with missing data out.

	Arguments:
	dm		--	DataMatrix

	Keyword arguments:
	checkCue		--	Indicates whether the cue phase should be checked.
						(default=True)
	checkPostSacc	--	Indicates whether the postSacc phase should be checked.
						(default=True)

	Returns:
	The filtered DataMatrix.
	"""

	dm = dm.addField('missing', dtype=int, default=0)
	count = 0
	for i in dm.range():
		missing = False
		if checkCue:
			a = TraceKit.getTrace(dm[i], signal='pupil', phase='cue', \
				lock='end', baseline=baseline, baselineLock=baselineLock,
				traceLen=preTraceLen, nanPad=False)
			if np.isnan(a.sum()):
				missing = True
		if checkPostSacc:
			a = TraceKit.getTrace(dm[i], signal='pupil', phase='postSacc', \
				lock='start', baseline=baseline, baselineLock=baselineLock,
				traceLen=postTraceLen, nanPad=False)
			if np.isnan(a.sum()):
				missing = True
		if missing:
			dm['missing'][i] = 1
			count += 1
	print 'Found %d (of %d) trials with missing data' % (count, len(dm))
	dm = dm.select('missing == 0')
	return dm

def latencyCorr(dm):

	"""
	Determines the correlation between saccade latency and the latency of the
	PLR.

	Arguments:
	dm		--	DataMatrix
	"""

	dm = dm.addField('saccLat2Bin', dtype=float)
	dm = dm.calcPerc('saccLat2', 'saccLat2Bin', keys=['subject_nr'], nBin=10)
	#dm = dm.select('cond == "onset"')
	l = [ ['subject_nr', 'cond', 'bin', 'saccLat', 't0'] ]
	colors = TangoPalette.brightColors[:] * 10
	for _dm in dm.group(['subject_nr', 'saccLat2Bin']):
		for cond in ('constant', 'onset'):
			__dm = _dm.select("cond == '%s'" % cond, verbose=False)
			dmWhite = __dm.select('saccCol == "white"', verbose=False)
			xAvg, yAvg, errAvg= TraceKit.getTraceAvg(__dm, signal='pupil', \
				phase='postSacc', traceLen=postTraceLen, baseline=baseline, \
				baselineLock=baselineLock)
			xWhite, yWhite, errWhite = TraceKit.getTraceAvg(dmWhite, \
				signal='pupil', phase='postSacc', traceLen=postTraceLen, \
				baseline=baseline, baselineLock=baselineLock)
			yWhite -= yAvg
			opts = fitCurve(xWhite, yWhite, plot=False)
			t0 = opts[0]
			subject = __dm['subject_nr'][0]
			col = colors[int(subject)]
			saccLat = __dm['saccLat2'].mean()
			_bin = __dm['saccLat2Bin'][0]
			plt.plot(saccLat, t0, 'o', color=col)
			l.append( [subject, cond, _bin, saccLat, t0] )
			print subject, t0, saccLat
	dm = DataMatrix(l)
	dm.save('output/%s/latencyCorr.csv' % exp)
	print dm
	#plt.plot(dm['saccLat'], dm['t0'], '.')
	s, i, r, p, se = linregress(dm['saccLat'], dm['t0'])
	print 'r = %.4f, p = %.4f' % (r, p)
	plt.plot(dm['saccLat'], i+s*dm['saccLat'])
	plt.show()

	newFig(size=(4.8, 2.4))
	plt.subplots_adjust(bottom=.2)
	pmX = PivotMatrix(dm, ['cond', 'bin'], ['subject_nr'], 'saccLat', \
		colsWithin=True, err='se')
	print pmX

	pmY = PivotMatrix(dm, ['cond', 'bin'], ['subject_nr'], 't0', \
		colsWithin=True, err='se')
	print pmY

	xM = np.array(pmX.m[-2, 2:-2], dtype=float)
	xErr = np.array(pmX.m[-1, 2:-2], dtype=float)
	xMConst = xM[:len(xM)/2]
	xMOnset = xM[len(xM)/2:]
	xErrConst = xErr[:len(xErr)/2]
	xErrOnset = xErr[len(xErr)/2:]

	yM = np.array(pmY.m[-2, 2:-2], dtype=float)
	yErr = np.array(pmY.m[-1, 2:-2], dtype=float)
	yMConst = yM[:len(yM)/2]
	yMOnset = yM[len(yM)/2:]
	yErrConst = yErr[:len(yErr)/2]
	yErrOnset = yErr[len(yErr)/2:]

	plt.errorbar(xMConst, yMConst, xerr=xErrConst, yerr=yErrConst, label= \
		'Constant', capsize=0, color=constColor, fmt='o-')
	plt.errorbar(xMOnset, yMOnset, xerr=xErrOnset, yerr=yErrOnset, label='Onset', \
		capsize=0, color=onsetColor, fmt='o-')
	plt.legend(frameon=False)
	plt.xlabel('Saccade latency (ms)')
	plt.ylabel('PLR latency (ms)')
	saveFig('latencyCorr')

	aov = AnovaMatrix(dm, ['cond', 'bin'], 't0', 'subject_nr')
	print aov
	aov.save('output/%s/aov.latencyCorr.csv' % exp)

def saccMetricsStats(dm):

	"""
	Analyzes the effect of condition on

	- Saccade end points
	- SOA
	- Error rate

	Arguments:
	dm		--	A DataMatrix
	"""

	from exparser.RBridge import RBridge
	global R
	try:
		R
	except:
		R = RBridge()

	cm = dm.collapse(['cond', 'subject_nr'], 'saccEndX')
	R.load(cm)
	am = R.aov('mean ~ cond + Error(subject_nr/cond)')
	am.save('output/%s/aov.saccEndX.csv' % exp)
	am = R.aov('count ~ cond + Error(subject_nr/cond)')
	am.save('output/%s/aov.cellCount.csv' % exp)
