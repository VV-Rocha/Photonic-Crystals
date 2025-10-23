from .utils import NpConversionMethods
from .device import DeviceMethods

class Arrayfire(DeviceMethods, NpConversionMethods):
    def __init__(
        self,
        device_config: dict,
        *args,
        **kwargs,
    ):
        """ Initialize the DeviceConfig class. 

        This class is used to configure the device and backend for arrayfire computations. 
        It sets the device and backend based on the input configuration. 

        Args:
            device_config (dict): The configuration dictionary for the device and backend. 
                It should contain keys "device" and "backend" with values int and str, respectively. For example:

        device_config = {
            "device": 0,
            "backend: "cuda",
        }
        """
        self.device = device_config["device"]
        self.backend = device_config["backend"]
        
        super().__init__(
            *args,
            **kwargs,
            )