import module
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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
        #print(f"MCS {self._time}")
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
        
        sizex = None
        sizey = None
        with open(parfile, 'r') as file:
            for line in file:
                if 'sizex' in line:
                    sizex = int(line.split(' = ')[1])

                if 'sizey' in line:
                    sizey = int(line.split(' = ')[1])
        if not sizex or not sizey:
            raise RuntimeError("Did not find sizes in the parameterfile!")

        self._drawing = np.zeros((2*sizex,2*sizey, 3)).astype(np.intc)

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

    def draw(self, ax):
        self.exporter.computeDrawing(self._drawing,1)
        ax.imshow(self._drawing)


    def runAndAnimate(self, runtime, draw_stride):

        fig, ax = plt.subplots() 
        
        im = ax.imshow(self._drawing)

        def init():
            im.set_array(self._drawing)
            return [im]

        def update(frame):
            self.TimeStep(draw_stride)
            self.exporter.computeDrawing(self._drawing, 1)
            im.set_array(self._drawing)
            print(f"Drawing frame %s" % (draw_stride*frame))
            return [im]

        ani = FuncAnimation(fig, update, 
                            frames=np.array(range( runtime // draw_stride)),
                            init_func=init,blit=True)     
        return ani
