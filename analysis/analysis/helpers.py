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
		plt.xlim(0, preTraceLen)

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
				plt.plot(xPost, blackPost-whitePost, ':', color=col,
					label='inverse swap')
		plt.legend(frameon=False)

		# Main plots
		i = 1
		for cond in ('constant', 'swap', 'onset'):
			print '\t%s' % cond
			__dm = _dm.select('cond == "%s"' % cond, verbose=False)
			_dmWhite = __dm.select('saccCol == "white"', verbose=False)
			_dmBlack = __dm.select('saccCol == "black"', verbose=False)
			ax = plt.subplot2grid((4,7), (i,0), colspan=1)
			ax.spines["right"].set_visible(False)
			ax.get_yaxis().tick_left()
			ax.axhline(1.0, linestyle='--', color='black')
			# Draw saccade onsets
			sMin = __dm['flipSDelay'].min()
			sMax = __dm['flipSDelay'].max()
			sMean = __dm['flipSDelay'].mean()
			plt.axvspan(preTraceLen-sMin, preTraceLen-sMax, color=flipSColor,
				alpha=.1)
			plt.axvline(preTraceLen-sMean, color=flipSColor,
			   linestyle=flipSStyle)
			tracePlot(__dm, traceParamsPre, suffix='.%s.%s.pre' % (cond, \
				subjectNr), err=True)

			plt.xticks(range(150, preTraceLen+1, 150), range(-preTraceLen+150,
				1, 150))
			if i < 3:
				ax.get_xaxis().set_ticklabels([])
			if cond == 'swap':
				plt.ylabel('Pupil size (norm.)')
			plt.xlim(0, preTraceLen)
			plt.ylim(yMin, yMax)

			# Post-saccade
			ax = plt.subplot2grid((4,7), (i,1), colspan=6)
			ax.spines["left"].set_visible(False)
			plt.axvline(0, linestyle='--', color='black')
			ax.axhline(1.0, linestyle='--', color='black')
			# Title
			plt.text(0.1, 0.9, cond, horizontalalignment='center',
				verticalalignment='center', transform=ax.transAxes)
			# Draw saccade offsets
			eMin = -__dm['flipEDelay'].min()
			eMax = -__dm['flipEDelay'].max()
			eMean = -__dm['flipEDelay'].mean()
			plt.axvspan(eMin, eMax, color=flipEColor, \
				alpha=.1)
			plt.axvline(eMean, color=flipEColor, linestyle=flipEStyle)
			tracePlot(__dm, traceParamsPost, suffix='.%s.%s.post' % (cond, \
				subjectNr), err=True)
			plt.ylim(yMin, yMax)
			plt.xlim(0, postTraceLen)
			if i == 3:
				plt.xlabel('Time after saccade (ms)')
			if i < 3:
				ax.get_xaxis().set_ticklabels([])
			plt.xticks(range(150, postTraceLen, 150))
			ax.get_yaxis().tick_right()
			ax.get_yaxis().set_ticklabels([])
			if cond == 'constant':
				plt.legend(frameon=False, loc='lower left')
			i += 1

		saveFig('main.subject.%s' % subjectNr, show=True)

@cachedArray
def lmeTrace(dm, traceParams, suffix=''):

	"""
	desc: |
		Performs the lme analysis for the cueLum Bright vs Dark contrast.

	arguments:
		dm:				A DataMatrix.
		traceParams:	The trace parameters.

	keywords:
		suffix:			A suffix to identify the trace.

	returns: |
		A 2D array where the columns are [p, ciHi, ciLo] and the rows are the
		samples.
	"""

	_dm = dm.selectColumns(['saccCol', 'subject_nr', '__trace_postSacc__',
		'__trace_cue__', '__trace_baseline__'])
	a = TraceKit.mixedModelTrace(_dm, traceModel, winSize=winSize,
		**traceParams)
	return a

def tracePlot(dm, traceParams, suffix='', err=True):

	"""
	desc: |
		A pupil-trace plot for a single epoch.

	arguments:
		dm:				A DataMatrix.
		traceParams:	The trace parameters.

	keywords:
		suffix:			A suffix to identify the trace.
		err:			Indicates whether error bars should be drawn.
	"""

	x1, y1, err1 = TraceKit.getTraceAvg(dm.select('saccCol == "white"'),
		**traceParams)
	x2, y2, err2 = TraceKit.getTraceAvg(dm.select('saccCol == "black"'),
		**traceParams)
	if err:
		d = y1-y2
		aErr = lmeTrace(dm, traceParams=traceParams, suffix=suffix,
			cacheId='lmeTrace%s' % suffix)
		aT = aErr[:,0]
		aLo = aErr[:,2]
		aHi = aErr[:,1]
		minErr = (d-aLo)/2
		maxErr = (aHi-d)/2
		y1min = y1 - minErr
		y1max = y1 + maxErr
		y2min = y2 - minErr
		y2max = y2 + maxErr
		plt.fill_between(x1, y1min, y1max, color=brightColor, label='Bright')
		plt.fill_between(x2, y2min, y2max, color=darkColor, label='Dark')
		TraceKit.markStats(plt.gca(), np.abs(aT), below=False, thr=2,
			minSmp=200, loExt=True, hiExt=True)
		plt.plot(x1, d, color='green')
	else:
		plt.plot(x1, y1, color=brightColor, label='Bright')
		plt.plot(x2, y2, color=darkColor, label='Dark')

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
	Analyzes the effect of condition on saccade landing position and error rate.

	Arguments:
	dm		--	A DataMatrix
	"""

	dm['saccEndX'] = dm['saccEndX'] - 512
	dm['saccEndX'][np.where(dm['saccSide'] == 'left')] *= -1
	cm = dm.collapse(['cond', 'subject_nr'], 'saccEndX')

	R().load(cm)
	am = R().aov('mean ~ cond + Error(subject_nr/cond)')
	am._print('SaccEndX')
	am.save('output/%s/aov.saccEndX.csv')
	am = R().aov('count ~ cond + Error(subject_nr/cond)')
	am._print('Count')
	am.save('output/%s/aov.cellCount.csv')

	aOnset = cm.select('cond == "onset"')['mean']
	aConstant = cm.select('cond == "constant"')['mean']
	aSwap = cm.select('cond == "swap"')['mean']
	print 'M(saccEndx, onset) = %.4f' % (aOnset.mean()/pxPerDeg)
	print 'M(saccEndx, const) = %.4f' % (aConstant.mean()/pxPerDeg)
	print 'M(saccEndx, swap) = %.4f' % (aSwap.mean()/pxPerDeg)

	aOnset = cm.select('cond == "onset"')['count']
	aConstant = cm.select('cond == "constant"')['count']
	aSwap = cm.select('cond == "swap"')['count']
	print 'M(count, onset) = %.4f' % (100 - 100.* (aOnset.mean()/120))
	print 'M(count, const) = %.4f' % (100 - 100.* (aConstant.mean()/120))
	print 'M(count, swap) = %.4f' % (100 - 100.* (aSwap.mean()/120))


def fixationStability(dm, offset=50):

	"""
	Determines the fixation stability during the post-saccade epoch for each
	of the conditions.

	Arguments:
	dm		--	A DataMatrix

	Keyword arguments:
	offset	--	The number of samples to skip at the beginning, to avoid taking
				into account the end of the saccade. (default=50)
	"""

	@cachedDataMatrix
	def addFixStabInfo(dm, offset):
		print 'Determining fixation stability ...'
		dm = dm.addField('fixStabX', dtype=float)
		for i in dm.range():
			a = TraceKit.getTrace(dm[i], signal='x', phase='postSacc',
				lock='start', offset=offset, traceLen=postTraceLen-offset,
				nanPad=False)
			print '%.4d\tM = %.2f, SD = %.2f' % (i, a.mean(), np.std(a))
			dm['fixStabX'][i] = np.std(a)
		print 'Done'
		return dm
	dm = addFixStabInfo(dm, offset, cacheId='fixStabInfo.%d' % offset)

	cm = dm.collapse(['cond', 'subject_nr'], 'fixStabX')
	R().load(cm)
	am = R().aov('mean ~ cond + Error(subject_nr/cond)')
	am._print('SaccEndX')
	am.save('output/%s/aov.fixStabX.csv')

	aOnset = cm.select('cond == "onset"')['mean']
	aConstant = cm.select('cond == "constant"')['mean']
	aSwap = cm.select('cond == "swap"')['mean']
	print 'M(fixStabX, onset) = %.4f' % (aOnset.mean()/pxPerDeg)
	print 'M(fixStabX, const) = %.4f' % (aConstant.mean()/pxPerDeg)
	print 'M(fixStabX, swap) = %.4f' % (aSwap.mean()/pxPerDeg)
