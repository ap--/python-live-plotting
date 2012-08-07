
from gi.repository import Gtk, GLib, Gdk

import collections
import random
import time
import math

class Ca:
    # requires GTK3 port of cagraph from 
    # > https://github.com/ap--/cagraph-1.2-gtk3.git
    from cagraph.ca_graph import CaGraph as Graph
    from cagraph.ca_graph_file import CaGraphFile as GraphFile
    from cagraph.axis.xaxis import CaGraphXAxis as GraphXAxis
    from cagraph.axis.yaxis import CaGraphYAxis as GraphYAxis
    from cagraph.axis.taxis import CaGraphTAxis as GraphTAxis
    from cagraph.ca_graph_grid import CaGraphGrid as GraphGrid
    from cagraph.series.line import CaGraphSeriesLine as GraphSeriesLine
    from cagraph.series.bar import CaGraphSeriesBar as GraphSeriesBar
    from cagraph.series.area import CaGraphSeriesArea as GraphSeriesArea


class DynamicPlotter(Gtk.Window):

    def __init__(self, sampleinterval=0.1, timewindow=10., size=(780,580)):
        Gtk.Window.__init__(self, title='Dynamic Plotting with CaGraph-1.2-gtk3')
        self._size = size
        self._interval = int(sampleinterval*1000)
        # Gtk stuff
        self.connect("destroy", lambda x : Gtk.main_quit())
        self.set_default_size(*size)

        # Data stuff
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.timetics = [sampleinterval*i for i in range(-self._bufsize,1)]

        # CaGraph stuff
        self.graph = Ca.Graph()
        self.xaxis, self.yaxis = (Ca.GraphXAxis(self.graph),
                                  Ca.GraphYAxis(self.graph))
        self.xaxis.min=self.timetics[0]
        self.xaxis.max=self.timetics[-1]
        
        self.graph.axiss.append(self.xaxis)
        self.graph.axiss.append(self.yaxis)
        self.graph.graph_style.width = self._size[0]
        self.graph.graph_style.height = self._size[1]
        series = Ca.GraphSeriesLine(self.graph, 0, 1)
        self.graph.seriess.append(series)

        self.graph.grid = Ca.GraphGrid(self.graph, 0, 1)

        self.updateplot()
        
        self.add(self.graph)
        self.graph.show()
        self.show_all()

    def getdata(self):
        frequency = 0.5
        noise = random.normalvariate(0., 1.)
        new = 10.*math.sin(time.time()*frequency*2*math.pi) + noise
        return new

    def updateplot(self):
        self.databuffer.append( self.getdata() )
        self.graph.seriess[0].data = list(zip(self.timetics, self.databuffer))
        self.graph.auto_set_yrange(1)
        self.graph.queue_draw()
        return True

    def run(self):
        GLib.timeout_add(self._interval, self.updateplot )
        Gtk.main()

if __name__ == '__main__':

    m = DynamicPlotter(sampleinterval=0.05, timewindow=10.)
    m.run()

