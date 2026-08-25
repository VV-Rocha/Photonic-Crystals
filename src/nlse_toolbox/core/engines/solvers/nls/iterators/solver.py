from .af_np_interface import AfNpInterface


class Iterator:
    """ Base iterator class for solvers."""    
    def solve(self, box):
        """ Main solve method to iterate through steps."""
        for z in range(self.Nsteps):
            self.step_solver(box)  # solves (in place) for the next step

            box.storage.store_step(
                box = box,
                index = z+1,
            )

            print(f"{z + 1} / {box.solver.mesh.Nz}", end="\r")


class AfIterator(Iterator):
    """ Iterator with arrayfire initialization."""
    def solve(self, box):
        self.init_af(box)
        super().solve(box)
        self.end_af(box)


class AfTimeSpaceAnalogIterator(
    AfIterator,
    AfNpInterface,
):
    """ Iterator for time-analog solvers with arrayfire initialization."""
    @property
    def Nsteps(self,):
        if not hasattr(self, '_Nsteps'):
            self._Nsteps = self.mesh.Nz
        return self._Nsteps
    
    @Nsteps.setter
    def Nsteps(self, value):
        self._Nsteps = value