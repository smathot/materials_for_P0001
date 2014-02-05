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

from matplotlib import pyplot as plt
from const import *
 
def saveFig(name, clear=True, show=False):
	
	"""
	A convenience function for saving figures.
	
	Arguments:
	name	--	The figure name.
	
	Keyword arguments:
	clear	--	Indicates whether the figure should be cleared. (default=True)
	show	--	Indicates whether the figure should be shown. (default=False)
	"""
	
	plt.savefig('plots/%s/svg/%s.svg' % (exp, name))
	plt.savefig('plots/%s/png/%s.png' % (exp, name))
	if show:
		plt.show()
	elif clear:
		plt.clf()
		
def newFig(size=(4.8, 4.8)):
	
	"""Creates a new figure of default size."""
	
	return plt.figure(figsize=size)
