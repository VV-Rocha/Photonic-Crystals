def _potential_function(
    potential,
    total_intensity,
    Isat,
):
    """ Potential Function.

    Args:
        potential (float): Scalar value of the potential coefficient.
        total_intensity (ndarray): Intensity field.
        Isat (float): Saturation intensity of the crystal.

    Returns:
        ndarray: Potential field. 
    """
    return potential * total_intensity/(Isat + total_intensity)

class SaturatedPotential:
    def potential_function(self, media):
        """ Potential Function.

        Returns:
            ndarray: Potential field.
        """
        return _potential_function(self.potential, self.get_total_intensity(), media.Isat)
    
    def get_total_intensity(self, beams):
        first = True
        for beam in beams.values():
            if first:
                total_intensity = beam.get_intensity()
                first = False
            else:
                total_intensity += beam.get_intensity()
        return total_intensity