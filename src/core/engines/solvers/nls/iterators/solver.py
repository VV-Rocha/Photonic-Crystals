class Iterator:
    """ Base iterator class for solvers."""    
    def solve(self,):
        """ Main solve method to iterate through steps."""
        for z in range(self.Nsteps):
            self.step_solver()  # solves (in place) for the next step

            self.store_step(z+1)

            print(f"{z + 1} / {self.Nz}", end="\r")
            
class AfIterator(Iterator):
    """ Iterator with arrayfire initialization."""
    def solve(self,):
        self.init_af()
        super().solve()
        self.end_af()
            
class AfTimeSpaceAnalogIterator(AfIterator):
    """ Iterator for time-analog solvers with arrayfire initialization."""
    @property
    def Nsteps(self,):
        if not hasattr(self, '_Nsteps'):
            self._Nsteps = self.Nz
        return self._Nsteps
    
    @Nsteps.setter
    def Nsteps(self, value):
        self._Nsteps = value