# defines Python module PyTST
import math
import random
import datetime

# class Interface sets up interface with C module libTST
class Interface:
    def __init__(self,parfile=""):            
        self._libTST = __import__("libTST")
        self.read_parfile(parfile)
        self.set_callback_wrapper(CallbackWrapper())
        self._libTST.lib.init_session()
        self.active_dish = False
        self.walltime = 0

    def __del__(self):
        self._libTST.lib.release()

    def _init_callbacks(self):
        @self._libTST.ffi.def_extern()
        def callback_init(sigma):
            return self.cb.init(sigma)

        @self._libTST.ffi.def_extern()
        def callback_copy_attempt(sigma,x,y,xp,yp,ext_DH,stiffness):
            return self.cb.copy_attempt(sigma,x,y,xp,yp,ext_DH,stiffness)

        @self._libTST.ffi.def_extern()
        def callback_timestep(sigma):
            return self.cb.timestep(sigma)
        
        self._libTST.lib.set_callback_init(self._libTST.lib.callback_init)
        self._libTST.lib.set_callback_copy_attempt(self._libTST.lib.callback_copy_attempt)
        self._libTST.lib.set_callback_timestep(self._libTST.lib.callback_timestep)

    def read_parfile(self,parfile):
        cparfile = self._libTST.ffi.new("char[]",parfile.encode('ascii'))
        self._libTST.lib.read_parfile(cparfile)
        
    def set_callback_wrapper(self,cb):
        self.cb = cb   # store callback for bookkeeping
        self.cb._set_copy_prob(self._libTST.lib.copy_prob)   # pass libTST copy_prob
        self._init_callbacks()   # interfacing with CFFI

    def set_walltime(self,time_string):
        t = datetime.datetime.strptime(time_string, "%H:%M:%S")
        dt = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        self.walltime = int(dt.total_seconds())   # store walltime in seconds

    def run(self,its):
        if not self.active_dish:
            self._libTST.lib.init_dish()
            self.active_dish = True
        self._libTST.lib.run(its,self.walltime,False)

    def run_upto(self,its):
        if not self.active_dish:
            self._libTST.lib.init_dish()
            self.active_dish = True
        self._libTST.lib.run(its,self.walltime,True)

    def reset(self):
        self._libTST.lib.init_dish()


        

# class CallbackWrapper defines (empty) wrapper for Python level callback mechanism
# in main code this wrapper should be subclass'ed
class CallbackWrapper:
    #def __init__(self):
    #    pass

    def _set_copy_prob(self,copy_prob): # invoked by CPM.set_callback_wrapper
        self.copy_prob = copy_prob

    def init(self,sigma):
        # called upon initialization of CPM code
        pass

    def copy_attempt(self,sigma,x,y,xp,yp,ext_DH,stiffness):
        # determines whether copy attempt gets accepted
        return self.copy_accept(ext_DH,stiffness)

    def copy_accept(self,DH,stiffness):
        # decide whehter copy gets accepted based on energy differential
        # return True when accepted
        p = self.copy_prob(DH,stiffness) # self.copy_prob is provided by libTST
        s = random.uniform(0,1)
        return s <= p

    def timestep(self,sigma):
        # called each Monte Carlo timestep
        pass

