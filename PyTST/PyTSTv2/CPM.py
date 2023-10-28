import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
import module


class Callback_PyTST:
    def __init__(self):
        self.set_cpp_callback(module.Callback())
        self._time = 0

    def set_cpp_callback(self, cppCallback):
        self.callback = cppCallback
        self.set_callbacks()

    def set_callbacks(self):
        self.callback.set_copyattempt(self.copy_attempt)
        self.callback.set_init(self.init)
        self.callback.set_timestep(self.timestep)
        print("Setted callbacks")

    def init(self, sigma):
        print("Init called")

    def copy_attempt(self, sigma, x, y, xp, yp, ext_DH, stiffness):
        return self.copy_prob(ext_DH, stiffness)

    def timestep(self, sigma):
        print(f"MCS {self._time}")
        self._time+=1

    def copy_prob(DH, stiffness):
        pass


class Interface:
    def __init__(self, parfile, cb=None):
        # Initalize TST exporter
        self.exporter = module.Exporter(parfile)
        if cb is None:
            cb = Callback_PyTST()
        self.callback_pytst = cb
        self.callback_pytst.copy_prob = self.exporter.copy_prob
        # Give pointer of Callback (from callbacks.h) back to exporter
        self.exporter.setCallback(self.callback_pytst.callback)
        self.exporter.dishInit()

    def TimeStep(self, count=1):
        for _ in range(count):
            self.exporter.timestep()

    def celltype(self, sigma):
        return self.exporter.getColorOfCell(sigma)

    @property
    def sigma(self):
        return self.exporter.getSigma()

    def set_spin_tocell(self, nx, ny):
        self.exporter.addspin(nx,ny, 1)

class Window(QtWidgets.QMainWindow):
    def __init__(self, interface: Interface):
        super().__init__()
        self.resize(400, 400)
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 400)
        # set a scaled pixmap to a w x h window keeping its aspect ratio
        self.label.setPixmap(canvas)

        self.interface = interface

        self.init_colormap(interface.exporter.getNumOfCells())
        self.start()

    def start(self):
        self.loop(10)
        button = QtWidgets.QPushButton("Play/Pauze")
        button.setCheckable(True)
        button.clicked.connect(self.runButtonPress)
        # self.setCentralWidget(self.label)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.label)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.loop(count=10))
        # self.timer.start(0)
        self.time_loops = False

    def loop(self, count):
        self.interface.TimeStep(count=count)
        self.draw_sigma(self.interface.sigma)

    def runButtonPress(self):
        if self.time_loops:
            self.time_loops = False
            self.timer.stop()
        else:
            self.time_loops = True
            self.timer.start(0)

    def init_colormap(self, N):
        print("init colormap for", N, "cells")
        pos = [0] + [i/N for i in range(1, N+1)]
        col = [QtGui.QColor('white')]
        for sigma in range(1, N+1):
            tau = self.interface.celltype(sigma)
            color = {
                    0: QtGui.QColor('gray'),
                    1: QtGui.QColor('cyan'),
                    2: QtGui.QColor('yellow'),
                    3: QtGui.QColor('red'),
                    4: QtGui.QColor('red'),
            }.get(tau)
            if color is None:
                raise NotImplementedError(f"Color for {i} is not implemented")
            col.append(color)
        self.colormap = pg.ColorMap(pos, col)

    def draw_sigma(self, sigma):
        self.label.clear()
        image = pg.ImageItem()
        image.setImage(np.array(sigma)[1:-1, 1:-1])
        # print(set(np.array(sigma).reshape(-1).tolist()))
        image.setColorMap(self.colormap)
        self.label.setPixmap(image.getPixmap().scaled(198*2, 198*2))

    def draw_sigma_tst(self, sigma):  # crude and slow
        self.label.clear()
        canvas = QtGui.QPixmap(400, 400)
        painter = QtGui.QPainter(canvas)
        npsigma = np.array(sigma)
        for y, row in enumerate(npsigma):
            for x, s in enumerate(row):
                if s > 1:
                    color = self.exporter.getColorOfCell(s)
                    qColor = QtGui.QColor('c')
                    if color == 1:
                        qColor = QtGui.QColor('c')
                    elif color == 2:
                        qColor = QtGui.QColor('red')
                    elif color == 3:
                        qColor = QtGui.QColor('yellow')
                    else:
                        print(f"Error {color}")
                    painter.setPen(qColor)
                    painter.drawPoint(2*x, 2*y)
                    painter.drawPoint(2*x+1, 2*y)
                    painter.drawPoint(2*x, 2*y+1)
                    painter.drawPoint(2*x+1, 2*y+1)
                else:
                    painter.setPen(QtGui.QColor('white'))
                    painter.drawPoint(2*x, 2*y)
                    painter.drawPoint(2*x+1, 2*y)
                    painter.drawPoint(2*x, 2*y+1)
                    painter.drawPoint(2*x+1, 2*y+1)
        painter.end()
        self.label.setPixmap(canvas)

if __name__ == '__main__':
    try:
        parameterfile = sys.argv[1]
    except:
        parameterfile = "sorting.par"
    app = QtWidgets.QApplication(sys.argv)
    interface = Interface(parameterfile)
    window = Window(interface)
    window.show()
    app.exec_()
