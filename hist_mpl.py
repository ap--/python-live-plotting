
from gi.repository import Gtk, GLib, Gdk, GObject
import collections
import random
import time

class mpl:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

import numpy as np


class Mplotter_nonthreaded(Gtk.Window):

    def __init__(self, interval=100, size=(400,300)):
        Gtk.Window.__init__(self)
        self.connect("destroy", lambda x : Gtk.main_quit())
        self.set_default_size(*size)
        self._interval = int(interval)
        self.d = collections.deque([0.0]*1000, 1000)
        self.a = np.zeros((1000,))
        self._bins = 30
        self._range = (0.0, 15.0)

        self.figure = mpl.Figure()
        self.subplt = self.figure.add_subplot(1, 1, 1)
        self.canvas = mpl.FigureCanvas(self.figure)
        self.add(self.canvas)

        self.set_keep_above(True)
        self.show_all()

        n, self.bins, self.patches = self.subplt.hist(self.a, 15, normed=True,
                                                        range=self._range)

    def update(self, t=[0.0]):
        self.d.append(random.lognormvariate(2.,0.2)) # almost nothing
        self.a[:] = self.d
        X, _ = np.histogram(self.a, bins=self.bins, normed=True)
        
        for rect, h in zip(self.patches, X):
            rect.set_height(h)
        self.subplt.autoscale(True)
        
        self.canvas.draw() # 20ms
        return True

    def run(self):
        GLib.timeout_add(self._interval, self.update)
        Gtk.main()

if __name__ == '__main__':

    m = Mplotter_nonthreaded(10)
    m.run()

