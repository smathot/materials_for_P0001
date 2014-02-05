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
from exparser import TraceKit, Fitting
import numpy as np
from const import *
from figure import *
from exparser.DataMatrix import DataMatrix
from scipy.stats import ttest_rel

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

def fitCurve(x, y, label=None, col='black', linewidth=1, plot=True):
	
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
	"""
	
	from scipy.optimize import curve_fit
		
	guess = [300, 500, -.2, 0]
	popt, pcov = curve_fit(pupilCurve, x, y, p0=guess)
	fit = pupilCurve(x, popt[0], popt[1], popt[2], popt[3])	
	if plot:
		plt.axhline(0, linestyle=':', color='black', linewidth=.5)
		plt.plot(x, y, '-', color=col, label=label, linewidth=linewidth)
		plt.plot(x, fit, ':', color=col, linewidth=linewidth)
		plt.axvline(popt[0], linestyle='--', color=col, linewidth=linewidth)
		plt.ylim(-.4, .1)
		plt.xlim(0, postTraceLen)
	return popt
	
def fit(dm, suffix=''):
	
	"""
	Fits the data based on an exponential pupil model.
	
	Arguments:
	dm		--	DataMatrix
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
			elif cond == 'onset':
				col = onsetColor
			else:
				col = swapColor
			opts = fitCurve(xWhite, yWhite, col=col, label=cond, \
				linewidth=linewidth)
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
	
