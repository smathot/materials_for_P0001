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
from exparser import TraceKit, Fitting, Plot
from exparser.Cache import cachedArray
import numpy as np
from const import *
from figure import *
from exparser.DataMatrix import DataMatrix
from exparser.RBridge import R
from scipy.stats import ttest_rel, nanmean, nanstd

def pupilCurve(x, t0=300., speed=500., lim1=-0.2, lim2=0.0):

	"""
	An exponential pupil model for a sustained pupillary response. This is an
	adaptation of the transient curve (see pupilTransientCurve()).

	Arguments:
	x		--	The x data, i.e. time.

	Keyword arguments:
	t0		--	The start of the function, i.e. the response latency.
				(default=300)
	speed	--	The speed of the curve, where higher values indicate a
				shallower slope. (default=500)
	lim1	--	The end value of the curve. (default=-.2)
	lim2	--	The start value of the curve. (default=0)

	Returns:
	The y data, i.e. pupil size.
	"""

	a = np.exp(-(x-t0)/speed)
	a[:t0] = 1
	return a * (lim2-lim1) + lim1

@cachedArray
def getDiffTrace(dm):

	"""desc: |
	The difference pupil trace, i.e. the difference between Land-on-Dark and
	Land-on-Bright trials.

	arguments:
		dm:		A DataMatrix.

	returns: |
		A difference trace.
	"""

	dmWhite = dm.select('saccCol == "white"', verbose=False)
	xAvg, yAvg, errAvg= TraceKit.getTraceAvg(dm, signal='pupil',
		phase='postSacc', traceLen=postTraceLen, baseline=baseline,
		baselineLock=baselineLock)
	xWhite, yWhite, errWhite = TraceKit.getTraceAvg(dmWhite,
		signal='pupil', phase='postSacc', traceLen=postTraceLen,
		baseline=baseline, baselineLock=baselineLock)
	yWhite -= yAvg
	return yWhite


def fitSwap(dm, suffix='all'):

	"""
	desc: |
		Performs a mixture-model of the swap condition.

	arguments:
		dm:			A DataMatrix,

	keywords:
		suffix:
			desc:	A suffix.
			type:	[str, unicode]

	returns:
		desc: |
			- None if suffix is 'all'
			- Otherwise An (i1, i2) tuple indicating the end of the preparation
			  period and the start of the non-preparation period.
		type:
			[tuple, None]
	"""


	dmSwap = dm.select('cond == "swap"', verbose=False)
	ySwap = getDiffTrace(dmSwap, cacheId='swapDiff%s.%s' % (exp, suffix))
	dmOnset = dm.select('cond == "onset"', verbose=False)
	yOnset = getDiffTrace(dmOnset, cacheId='onsetDiff%s.%s' % (exp, suffix))
	dmConst= dm.select('cond == "constant"', verbose=False)
	yConst = getDiffTrace(dmConst, cacheId='constDiff%s.%s' % (exp, suffix))
	lP = []
	lErr = []
	for i in np.arange(1000):
		y1 = yConst[i]
		y2 = yOnset[i]
		y3 = ySwap[i]
		pBest = None
		errBest = None
		for p in np.linspace(0, 1, 1000):
			y3est = p*-y1 + (1-p)*y2
			err = abs(y3est-y3)
			if errBest == None or err < errBest:
				errBest = err
				pBest = p
		lP.append(pBest)
		lErr.append(errBest)
	aP = np.array(lP)
	fig = newFig(size=flat)
	plt.ylim(-.1, 1.1)
	plt.axhline(0, linestyle=':', color='black')
	plt.axhline(1, linestyle=':', color='black')
	plt.yticks(np.linspace(0,1,6))
	plt.ylabel('Preparation index')
	plt.xlabel('Time relative to display change (ms)')
	if suffix == 'all':
		# Values hard-coded based on fitSwapAll() output
		plt.axvspan(352.50-1.96*13.22, 352.50+1.96*13.22, color=brown[1],
			alpha=.1)
		plt.axvline(352.50, color=brown[1], linestyle='--')
	else:
		lRoi = TraceKit.markStats(plt.gca(), aP, thr=.5, below=False,
			color=green[0])
		if len(lRoi) != 1:
			i1 = np.nan
		else:
			i1 = lRoi[0][1]
		lRoi = TraceKit.markStats(plt.gca(), aP, thr=.5, below=True, color=red[0])
		if len(lRoi) != 1:
			i2 = np.nan
		else:
			i2 = lRoi[0][0]
	plt.plot(aP, color=blue[1])
	saveFig('fitSwap/%s' % suffix)
	if suffix != 'all':
		return i1, i2

def fitSwapAll(dm):

	"""
	desc: |
		Performs the fitSwap() procedure for all participants separately.
	"""

	l1 = []
	l2 = []
	for _dm in dm.group('subject_nr'):
		i1, i2 = fitSwap(_dm, suffix='subject%d' % _dm['subject_nr'][0])
		l1.append(i1)
		l2.append(i2)
	print l1
	print 'Before preparation: M = %.2f, SE = %.2f' % (nanmean(l1),
		nanstd(l1)/np.sqrt(len(l1)))
	print l2
	print 'After preparation: M = %.2f, SE = %.2f' % (nanmean(l2),
		nanstd(l2)/np.sqrt(len(l2)))

def fitCurve(x, y, label=None, col='black', linewidth=1, plot=True,
	lineStyle='-'):

	"""
	Fits a single pupil trace and plots this as a single line.

	Arguments:
	x		--	The x-data, i.e. time.
	y		--	The y-data, i.e. pupil size.

	Keyword arguments:
	label		--	The plot label for the lines. (default=None)
	col			--	The plot color for the lines. (default='black')
	linewidth	--	The plot linewidth. (default=1)
	plot		--	Indicates whether the curve should be plotted.
					(default=True)
	lineStyle	--	The line style for the data. (default='-')
	"""

	from scipy.optimize import curve_fit

	guess = [300, 500, -.2, 0]
	popt, pcov = curve_fit(pupilCurve, x, y, p0=guess)
	fit = pupilCurve(x, popt[0], popt[1], popt[2], popt[3])
	if plot:
		plt.axhline(0, linestyle=':', color='black', linewidth=.5)
		plt.plot(x, y, lineStyle, color=col, label=label, linewidth=linewidth)
		plt.plot(x, fit, ':', color=col, linewidth=linewidth)
		plt.axvline(popt[0], linestyle='--', color=col, linewidth=linewidth)
		plt.ylim(-.4, .1)
		plt.xlim(0, postTraceLen)
	return popt

def fit(dm, suffix='', maxSmp=None):

	"""
	Fits the data based on an exponential pupil model.

	Arguments:
	dm		--	DataMatrixpass

	Keyword arguments:
	suffix	--	A suffix for the output files. (default='')
	maxSmp	--	The maximum number of samples to base the fit on, or None for
				no limit. (default=None)
	"""

	fig = newFig(size=bigWide)
	plt.subplots_adjust(wspace=0, hspace=0)
	i = 0

	l = [['subjectNr', 't0Const', 'speedConst', 'lim1Const', 'lim2Const', \
		't0Onset', 'speedOnset', 'lim1Onset', 'lim2Onset']]

	for dm in [dm] + dm.group('subject_nr'):

		print 'Subject %s' % i
		row = [i]

		# We use a 6 x 2 plot grid
		# XX X X X X
		# XX X X X X
		if i == 0:
			# Overall plot
			ax = plt.subplot2grid((2,6),(0,0), colspan=2, rowspan=2)
			# Draw 'window of preparation'
			plt.axvspan(0, prepWin, color=green[1], alpha=.2)
			linewidth = 1
			title = 'Full data (N=%d)' % len(dm.select('cond != "swap"'))
		else:
			# Individual plots
			ax = plt.subplot2grid((2,6),((i-1)/4, 2+(i-1)%4))
			linewidth = 1
			title = '%d (N=%d)' % (i, len(dm.select('cond != "swap"')))

		plt.text(0.9, 0.1, title, horizontalalignment='right', \
			verticalalignment='bottom', transform=ax.transAxes)

		if i == 0:
			plt.xticks([0, 500, 1000, 1500])
		elif i > 0 and i < 5:
			plt.xticks([])
		else:
			plt.xticks([0, 1000])
		if i > 0:
			plt.yticks([])
		else:
			plt.yticks([0, -.1, -.2, -.3])
		for cond in ('constant', 'onset'):
			_dm = dm.select("cond == '%s'" % cond, verbose=False)
			dmWhite = _dm.select('saccCol == "white"', verbose=False)
			xAvg, yAvg, errAvg= TraceKit.getTraceAvg(_dm, signal='pupil', \
				phase='postSacc', traceLen=postTraceLen, baseline=baseline, \
				baselineLock=baselineLock)
			xWhite, yWhite, errWhite = TraceKit.getTraceAvg(dmWhite, \
				signal='pupil', phase='postSacc', traceLen=postTraceLen, \
				baseline=baseline, baselineLock=baselineLock)
			yWhite -= yAvg
			if cond == 'constant':
				col = constColor
				lineStyle = '-'
			elif cond == 'onset':
				col = onsetColor
				lineStyle = '--'
			else:
				col = swapColor
				lineStyle = '-'
			if maxSmp != None:
				xWhite = xWhite[:maxSmp]
				yWhite = yWhite[:maxSmp]
			opts = fitCurve(xWhite, yWhite, col=col, label=cond, \
				linewidth=linewidth, lineStyle=lineStyle)
			print 't0 = %.4f, s = %.4f, l1 = %.4f, l2 = %.4f' % tuple(opts)
			t0 = opts[0]
			if i > 0:
				row += list(opts)
			else:
				plt.legend(frameon=False, loc='upper right')
			print '%s : %f' % (cond, t0)
		if i > 0:
			l.append(row)
		i += 1
	saveFig('fit%s' % suffix, show=False)
	dm = DataMatrix(l)
	dm.save('output/%s/fit%s.csv' % (exp, suffix))

	# Summarize the data and perform ttests on the model parameters
	for dv in ['t0', 'speed', 'lim1', 'lim2']:
		print'\nAnalyzing %s' % dv
		aConst = dm['%sConst' % dv]
		aOnset = dm['%sOnset' % dv]
		print 'Constant: M = %f, SE = %f' % (aConst.mean(), \
			aConst.std() / np.sqrt(N))
		print 'Onset: M = %f, SE = %f' % (aOnset.mean(), \
			aOnset.std() / np.sqrt(N))
		t, p = ttest_rel(aConst, aOnset)
		print 'Const vs onset, t = %.4f, p = %.4f' % (t, p)
		# Bayesian estimation (t-test)

def splitFit(dm):

	"""
	Similar to fit() expect that it performs separate analyses for fast vs slow
	saccadic eye movements.

	Arguments:
	dm		--	DataMatrix
	"""

	dm = dm.addField('saccLat2Bin', dtype=float)
	dm = dm.calcPerc('saccLat2', 'saccLat2Bin', keys=['subject_nr'], nBin=2)
	fit(dm.select('saccLat2Bin == 0'), suffix='.fast')
	fit(dm.select('saccLat2Bin == 50'), suffix='.slow')

def prepFit(dm, suffix=''):

	"""
	Perform a linear-regression fit on only the first 220 ms.

	Arguments:
	dm		--	DataMatrix

	Keyword arguments:
	suffix	--	A suffix for the output files. (default='')
	"""

	fig = newFig(size=bigWide)
	plt.subplots_adjust(wspace=0, hspace=0)
	i = 0

	l = [['subjectNr', 'sConst', 'iConst', 'sOnset', 'iOnset', 'sSwap',
		'iSwap']]

	for dm in [dm] + dm.group('subject_nr'):

		print 'Subject %s' % i
		row = [i]

		# We use a 6 x 2 plot grid
		# XX X X X X
		# XX X X X X
		if i == 0:
			# Overall plot
			ax = plt.subplot2grid((2,6),(0,0), colspan=2, rowspan=2)
			linewidth = 1
			title = 'Full data (N=%d)' % len(dm.select('cond != "swap"'))
		else:
			# Individual plots
			ax = plt.subplot2grid((2,6),((i-1)/4, 2+(i-1)%4))
			linewidth = 1
			title = '%d (N=%d)' % (i, len(dm.select('cond != "swap"')))

		plt.text(0.9, 0.1, title, horizontalalignment='right', \
			verticalalignment='bottom', transform=ax.transAxes)

		if i == 0:
			plt.xticks([0, 50, 100, 150, 200])
		elif i > 0 and i < 5:
			plt.xticks([])
		else:
			plt.xticks([0, 100])
		if i > 0:
			plt.yticks([])
		else:
			plt.yticks([0, -.01, -.02])
		plt.ylim(-.025, .01)
		plt.axhline(0, color='black', linestyle=':')
		for cond in ('constant', 'onset', 'swap'):
			_dm = dm.select("cond == '%s'" % cond, verbose=False)
			dmWhite = _dm.select('saccCol == "white"', verbose=False)
			xAvg, yAvg, errAvg= TraceKit.getTraceAvg(_dm, signal='pupil', \
				phase='postSacc', traceLen=postTraceLen, baseline=baseline, \
				baselineLock=baselineLock)
			xWhite, yWhite, errWhite = TraceKit.getTraceAvg(dmWhite, \
				signal='pupil', phase='postSacc', traceLen=postTraceLen, \
				baseline=baseline, baselineLock=baselineLock)
			yWhite -= yAvg
			xWhite = xWhite[:prepWin]
			yWhite = yWhite[:prepWin]
			if cond == 'constant':
				col = constColor
				lineStyle = '-'
			elif cond == 'onset':
				col = onsetColor
				lineStyle = '--'
			else:
				col = swapColor
				lineStyle = '-.'
				yWhite *= -1
			opts = Plot.regress(xWhite, yWhite, lineColor=col, symbolColor=col,
				label=cond, annotate=False, symbol=lineStyle, linestyle=':')
			s = 1000.*opts[0]
			_i = 1000.*opts[1]
			print 's = %.4f, i = %.4f' % (s, _i)
			if i > 0:
				row += [s, _i]
			else:
				plt.legend(frameon=False, loc='upper right')
		if i > 0:
			l.append(row)
		i += 1
	saveFig('linFitPrepWin%s' % suffix, show=False)
	dm = DataMatrix(l)
	dm.save('output/%s/linFitPrepWin%s.csv' % (exp, suffix))

	# Summarize the data and perform ttests on the model parameters
	for dv in ['s', 'i']:
		print'\nAnalyzing %s' % dv
		aConst = dm['%sConst' % dv]
		aOnset = dm['%sOnset' % dv]
		aSwap = dm['%sSwap' % dv]
		print 'Constant: M = %f, SE = %f' % (aConst.mean(), \
			aConst.std() / np.sqrt(N))
		print 'Onset: M = %f, SE = %f' % (aOnset.mean(), \
			aOnset.std() / np.sqrt(N))
		print 'Swap: M = %f, SE = %f' % (aSwap.mean(), \
			aSwap.std() / np.sqrt(N))
		# Standard t-tests
		t, p = ttest_rel(aConst, aOnset)
		print 'Const vs onset, t = %.4f, p = %.4f' % (t, p)
		t, p = ttest_rel(aSwap, aOnset)
		print 'Swap vs onset, t = %.4f, p = %.4f' % (t, p)
		t, p = ttest_rel(aConst, aSwap)
		print 'Const vs swap, t = %.4f, p = %.4f' % (t, p)

def blockPrepFit(dm):

	"""
	Perform the prepFit analysis separately for the first and second half of the
	experiment.

	Arguments:
	dm		--	A DataMatrix.
	"""

	dm1 = dm.select('count_block_sequence <= 4')
	dm2 = dm.select('count_block_sequence > 4')
	prepFit(dm1, suffix='.firstHalf')
	prepFit(dm2, suffix='.secondHalf')
