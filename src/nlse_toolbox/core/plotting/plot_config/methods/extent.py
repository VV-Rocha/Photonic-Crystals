def _float_to_extent(limit):
        return (
            -limit/2,
            limit/2,
            -limit/2,
            limit/2,
        )


class Extent:
    def set_extent(
        self,
        limits,
    ):
        """
        Defines the variable extent

        Args:
            limits (float, tuple of floats or list of floats): Limits of the axis. If float the limits are [-limits/2, limits/2]. If tuple of list the limits have the form [-limits/2, limits/2].
        """
        if (type(limits)==float):
            self.extent = _float_to_extent(limits * self.units_factor)
        elif ((type(limits)==tuple) or (type(limits)==list)):
            limits = (limits[i]*self.units_factor for i in range(len(limits)))
            if (len(limits)==4):
                self.extent = limits
            elif (len(limits)==2):
                self.extent = (
                    limits[0],
                    limits[1],
                    limits[0],
                    limits[1],
                )