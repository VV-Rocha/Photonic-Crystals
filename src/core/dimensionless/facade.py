from .decorators import checkpoint


class DimensionlessMethods:
    @checkpoint
    def adimensionalize_length(
        self,
        length,
        ):
        """Adimensionalize length.

        Args:
            length (float | ndarray): Dimensional length to be adimensionalized.

        Returns:
            float | ndarray: Adimensional length.
        """
        return length / self.transversal_adim_factor

    @checkpoint
    def dimensionalize_length(self, length):
        """Dimensionalize length.

        Args:
            length (float | ndarray): Adimensional length to be dimensionalized.

        Returns:
            float | ndarray: Dimensional length.
        """
        return length * self.transversal_adim_factor
    
    @checkpoint
    def adimensionalize_time(self, time):
        """Adimensionalize time.

        Args:
            time (float | ndarray): Dimensional time to be adimensionalized.

        Returns:
            float | ndarray: Adimensional time.
        """
        return time / self.longitudinal_adim_factor
    
    @checkpoint
    def dimensionalize_time(self, time):
        """Dimensionalize time.

        Args:
            time (float | ndarray): Adimensional time to be dimensionalized.

        Returns:
            float | ndarray: Dimensional time.
        """
        return time * self.longitudinal_adim_factor