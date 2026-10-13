from .af_np_interface import AfNpInterface


class Iterator:
    """ Base iterator class for solvers."""    
    def _solve(self, box):
        """ Main solve method to iterate through steps."""
        box.storage.store_step(
                        box = box,
                        index = 0,
                    )
        
        for z in range(self.Nsteps):
            self.step_solver(box)  # solves (in place) for the next step

            if ((z+1)%box.storage.stride == 0):
                box.storage.store_step(
                    box = box,
                    index = z+1,
                )
            
            if hasattr(self, "metadata"):
                self.compute_metadata(
                    i=z+1,
                    box = box,
                )

            self._print_iteration(
                z,
                box = box,
            )

    def get_metadata_print(
        self,
        z,
    ):
        txt = "; "
        for beam in self.metadata_history.keys():
            txt += beam + ": "
            for metadata in self.metadata_history[beam].keys():
                txt += metadata + f"-> {self.metadata_history[beam][metadata][z+1]}; "
        return txt
    
    def _print_iteration(
        self,
        z,
        box,
    ):
        if (self.verbose==0):
            pass
        elif (self.verbose==1):
            print(f"{z + 1} / {box.solver.mesh.Nz}", end="\r")
        elif (self.verbose==2):
            if hasattr(self, "metadata"):
                txt = f"{z + 1} / {box.solver.mesh.Nz}"
                metadata_txt = self.get_metadata_print(
                    z = z,
                )
                print(txt + metadata_txt)
            else:
                print(f"{z + 1} / {box.solver.mesh.Nz}; No metadata is called.", end="\r")

class AfIterator(Iterator):
    """ Iterator with arrayfire initialization."""
    def solve(self, box):
        self.init_af(box)
        super()._solve(box)
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