#!/usr/bin/env python

import numpy as np
from exparser.TangoPalette import *
from matplotlib import pyplot as plt

t0=295.7
speed=456.9
lim1=-0.2938
lim2=-0.0063

def pupilCurve(x):
	
	a = np.exp((-x+t0)/speed)
	a[:t0] = 1
	return a * (lim2-lim1) + lim1

plt.rc('font', family='Arial', size=10)
plt.figure(figsize=(2,2))

xData = np.linspace(0, 2999, 3000)
yData = pupilCurve(xData)

plt.axhline(lim1, linestyle='--', color=orange[1])
plt.axhline(lim2, linestyle='--', color=green[1])
plt.axvline(t0, linestyle='--', color=red[1])
plt.xlabel('t')
plt.ylabel('p(t)')

#plt.text(1000, -.1, r'$where t >= t0: p(t) = e^ \frac{-t+t0}{s} \cdot (p1-p2) + p2$')
#plt.text(1000, -.15, r'$where t < t0: p(t) = 0$')

plt.ylim(-.4, .1)

plt.plot(xData, yData, color=blue[1], linewidth=2)
plt.savefig('expExample.svg')
plt.show()
