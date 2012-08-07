
from gi.repository import Gtk, GLib

import collections
import random
import time
import math

class mpl:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

class DynamicPlotter(Gtk.Window):

    def __init__(self, sampleinterval=0.1, timewindow=10., size=(600,350)):
        # Gtk stuff
        Gtk.Window.__init__(self, title='Dynamic Plotting with Matplotlib + Gtk3')
        self.connect("destroy", lambda x : Gtk.main_quit())
        self.set_default_size(*size)
        # Data stuff
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = [sampleinterval*i for i in range(-self._bufsize+1,1)]
        # MPL stuff
        self.figure = mpl.Figure()
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.grid(True)
        self.canvas = mpl.FigureCanvas(self.figure)
        self.line, = self.ax.plot(self.x, self.databuffer)
        # Gtk stuff
        self.add(self.canvas)
        self.canvas.show()
        self.show_all()

    def getdata(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        return new

    def updateplot(self):
        self.databuffer.append( self.getdata() )
        self.line.set_ydata(self.databuffer)
        self.ax.relim()
        self.ax.autoscale_view(False, False, True)
        self.canvas.draw()
        return True

    def run(self):
        GLib.timeout_add(self._interval, self.updateplot )
        Gtk.main()

if __name__ == '__main__':

    m = DynamicPlotter(sampleinterval=0.05, timewindow=10.)
    m.run()

