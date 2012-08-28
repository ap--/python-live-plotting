
import visvis as vv

import collections
import random
import time
import math
import numpy as np

class DynamicPlotter():

    def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        # Visvis stuff
        self.app = vv.use('qt4')
        vv.title('Dynamic Plotting with VisVis')
        self.line = vv.plot(self.x, self.y, lc='b', lw=3, ms='+')
        vv.xlabel('time')
        vv.ylabel('amplitude')
        self.ax = vv.gca()

        self.timer = vv.Timer(self.app, 50, oneshot=False)
        self.timer.Bind(self.updateplot)
        self.timer.Start()

    def getdata(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        return new

    def updateplot(self, timer):
        self.databuffer.append( self.getdata() )
        self.y[:] = self.databuffer
        self.line.SetYdata(self.y)
        self.ax.SetLimits()
        return True

    def run(self):
        self.app.Run()

if __name__ == '__main__':

    m = DynamicPlotter(sampleinterval=0.05, timewindow=10.)
    m.run()

