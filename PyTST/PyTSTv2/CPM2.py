import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
import module
class Callback_PyTST:
    def __init__(self):
        self.set_cpp_callback(module.Callback())
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
    def copy_attempt(self, sigma, x,y,xp,yp, ext_DH, stiffness):
        print("Copy attempt called")
        return 1
    def timestep(self, sigma):
        print("MCS")
    def copy_prob(DH, stiffness):
        pass

class Interface(QtWidgets.QMainWindow):
    def __init__(self, parfile, cb = None):
        super().__init__()
        self.resize(400,400)
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 400)
        # set a scaled pixmap to a w x h window keeping its aspect ratio
        self.label.setPixmap(canvas)

        if cb is None:
            cb = Callback_PyTST()
        self.callback_pytst =cb

        # Initalize TST exporter
        self.exporter = module.Exporter(parfile)
        self.callback_pytst.copy_prob = self.exporter.copy_prob
        # Give pointer of Callback (from callbacks.h) back to exporter
        self.exporter.setCallback(self.callback_pytst.callback)
        self.exporter.dishInit()
        self.init_colormap(self.exporter.getNumOfCells())
        self.start()
    def start(self):
        self.TimeStep(10)

        button = QtWidgets.QPushButton("Play/Pauze")
        button.setCheckable(True)
        button.clicked.connect(self.runButtonPress)
        #self.setCentralWidget(self.label)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.label)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.TimeStep(count=10))
        #self.timer.start(0)
        self.time_loops = False

    def loop(self, count):
        for _ in range(count):
            self.TimeStep()
    def TimeStep(self, count = 1):
        for _ in range(count):
            self.exporter.timestep()
        self.draw_sigma(self.exporter.getSigma())
    def runButtonPress(self):
        if self.time_loops:
            self.time_loops = False
            self.timer.stop()
        else:
            self.time_loops = True
            self.timer.start(0)
    def init_colormap(self, N):
        pos = [0] + [i/N for i in range(1,N+1)]
        col = [QtGui.QColor('white')]
        for i in range(1,N+1):
            k = self.exporter.getColorOfCell(i)
            if k == 2:
                col.append(QtGui.QColor('yellow'))
            elif k == 3:
                col.append(QtGui.QColor('red'))
            elif k == 1:
                col.append(QtGui.QColor('cyan'))
                print("Cyan")
            else:
                raise Exception(f"Color error {k}")
        self.colormap = pg.ColorMap(pos, col)
    def draw_sigma(self, sigma):
        self.label.clear()
        image = pg.ImageItem()
        image.setImage(np.array(sigma)[1:-1,1:-1])
        #print(set(np.array(sigma).reshape(-1).tolist()))
        image.setColorMap(self.colormap)
        self.label.setPixmap(image.getPixmap().scaled(198*2,198*2))
    def draw_sigma_tst(self, sigma): # crude and slow
        self.label.clear()
        canvas = QtGui.QPixmap(400, 400)
        painter = QtGui.QPainter(canvas)
        npsigma = np.array(sigma)
        for y,row in enumerate(npsigma):
            for x,s in enumerate(row):
                if s>1:
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
                    painter.drawPoint(2*x,2*y)
                    painter.drawPoint(2*x+1,2*y)
                    painter.drawPoint(2*x,2*y+1)
                    painter.drawPoint(2*x+1,2*y+1)
                else:
                    painter.setPen(QtGui.QColor('white'))
                    painter.drawPoint(2*x,2*y)
                    painter.drawPoint(2*x+1,2*y)
                    painter.drawPoint(2*x,2*y+1)
                    painter.drawPoint(2*x+1,2*y+1)
        painter.end()
        self.label.setPixmap(canvas)
    def __del__(self):
        del self.exporter
if __name__ == '__main__':
    try:
        parameterfile = sys.argv[1]
    except:
        parameterfile = "sorting.par"
    app = QtWidgets.QApplication(sys.argv)
    window = Interface(parameterfile)
    window.show()
    app.exec_()
