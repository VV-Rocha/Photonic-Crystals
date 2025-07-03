from arrayfire import constant, set_backend, set_device

from numpy import ndarray

from functools import wraps
from copy import deepcopy

class Solver:
    """Wrapper class for the coupled equations solver."""
    def __init__(self,
                 mesh,
                 coefs,
                 solver_method,
                 precision_control,
                 device=0,
                 gpu_backend="cuda",
                 storing_method=None,
                 ):
        """Simulation functions.

        Args:
            mesh (Mesh object): Mesh object containing the mesh information for the simulation.
            coefs (Coefs object): Object containing the coefficients for the equation solved by the solver_method
            solver_method (func): Function that implements the solver method. It should be a function that takes the fields and the mesh as input and returns the updated fields.
            precision_control (PrecisionControl): PrecisionControl object that contains the numerical precision information for the simulation.
            device (int, optional): Device to be used to calculate the solutions. Defaults to 0.
            gpu_backend (str, optional): If using gpu should it use 'cuda' or 'opencl'. Defaults to 'cuda'.
            storing_method (StoreConfig, optional): StoreConfig object containing the directories in which to store the states. Defaults to None.
        """
        # Choose device:
        self.device = device
        self.gpu_backend = gpu_backend
        self.set_device()
        # Initialize precision variables
        self.precision_control = precision_control
        
        # Define solver method
        self.solver_method = solver_method
                
        # start meshes
        self.mesh = mesh
        self.mesh.init_k_mesh()
        
        self.coefs = coefs
        
        self.storing_method = storing_method
    
    def copy_input(func):
        @wraps(func)
        def wrapper(self, fields, *args, **kwargs):
            if fields.nfields == "coupled":
                fields.copy_input_fields()
            elif fields.nfields == "single":
                fields.copy_input_field()
            return func(self, fields, *args, **kwargs)
        return wrapper
    
    def input_fields_to_arrs(solver):
        @wraps(solver)
        def wrapper(self, fields, *args, **kwargs):
            if self.solver_method.numerical == "Arrayfire":
                from ..core.mesh import AfMesh2D
                self.af_mesh = AfMesh2D(self.mesh, self.precision_control)
                self.af_mesh.init_k_mesh()
                
                if fields.nfields == "single":
                    from ..fields import AfField2D
                    fields = AfField2D(fields)
                elif fields.nfields == "coupled":
                    from ..fields import AfCoupledFields2D
                    fields = AfCoupledFields2D(fields)
                     
            solver(self, fields, *args, **kwargs)
            
            if fields.nfields == "single":
                fields.update_Field()
            elif fields.nfields == "coupled":
                fields.update_Fields()
            
        return wrapper
    
    @copy_input
    @input_fields_to_arrs
    def solver(self, fields, store_config=None):
        """Solves the equation using the solver method and the fields provided.

        Args:
            fields (Fields object): Fields object containing the fields to be solved.
            return_flag (bool, optional): If True returns the Fields object. Defaults to False.
            store_config (StoreConfig object, optional): StoreConfig object containing the directories to store the states. Defaults to None.

        Returns:
            Fields: Fields object containing the solved fields.
        """
        for _t in range(1, self.mesh.Nz):
            # Single step simulation
            self.solver_method.solver(fields,
                                      mesh = self.af_mesh,
                                      coefs = self.coefs,
                                      precision_control = self.precision_control,
                                      )

            # % TODO: Stride storage is still not functional. Among the reasons is that striding method has not been implemented and all files having the same name are being overwritten.
            if hasattr(store_config, "get_store_type"):
                if (store_config.get_store_type() == "stride"):    
                    fields.store_fields(_t)
        if hasattr(store_config, "get_store_type"):
            if (store_config.get_store_type() == "last"):
                fields.store_fields(index = "last",
                                    )

    def set_device(self):
        """
        Set the ArrayFire device and configure the default data types.
        
        If using GPU (i.e. device is not 'cpu'), the GPU backend is chosen based on self.gpu_backend (either 'cuda' or 'opencl') and 32-bit floats and 64-bit complex numbers are enforced. If using 'cpu', then the CPU backend is selected and 64-bit types are allowed.
        """
        if isinstance(self.device, str) and self.device.lower() == "cpu":
            set_backend("cpu")
            print("Using CPU backend with float64 and complex128")
        else:
            try:
                device_id = int(self.device)
                # Choose GPU backend based on self.gpu_backend
                if self.gpu_backend.lower() == "cuda":
                    set_backend("cuda")
                    backend_used = "CUDA"
                else:
                    set_backend("opencl")
                    backend_used = "OpenCL"
                set_device(device_id)
                # On GPU, ArrayFire supports 32-bit floats and corresponding 64-bit complex numbers.
                # print(f"Using GPU backend ({backend_used}) on device {device_id} with float32 and complex64")
            except Exception as e:
                raise ValueError("Invalid device specifier. Use 'cpu' or a GPU device number as a string or integer.") from e