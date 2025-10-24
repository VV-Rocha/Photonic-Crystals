class Iterator:
    """ Base iterator class for solvers."""    
    def solve(self,):
        """ Main solve method to iterate through steps."""
        for z in range(self.Nsteps-1):
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
        return self.Nz