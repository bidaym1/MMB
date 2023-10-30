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

