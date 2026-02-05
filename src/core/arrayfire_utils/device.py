import arrayfire as af

class DeviceMethods:
    def set_device(self,):
        """
        Set the arrayfire device based on the configuration. 
        This method is called during initialization and sets the device for all subsequent computations.
        """
        # af.set_backend(self.backend)
        af.set_device(self.device)
        print("Backend:", af.get_active_backend())
        print(af.info()) 