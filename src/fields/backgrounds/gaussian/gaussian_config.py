from ...utils import float_to_tuple


class GaussianConfig1D:
    """ 1D Gaussian background field configuration."""
    def __init__(
        self,
        envelope_config: dict,
        *args,
        **kwargs,
        ):
        """ Initialize the Gaussian configuration.

        Args:
            envelope_config (dict): Configuration dictionary for the Gaussian envelope. keys include:
                - "I": Intensity of the Gaussian envelope.
                - "width": Width of the Gaussian envelope.
                - "center": Center position of the Gaussian envelope.
                - "exponent": Exponent for the Gaussian envelope.
        """
        self.I = envelope_config["I"]
        self.width = envelope_config["width"]
        self.center = envelope_config["center"]
        self.exponent = envelope_config["exponent"]
        super().__init__(
            *args,
            **kwargs,
            )
        
    def adimensionalize_envelope(self,):
        """ Adimensionalize the parameters of the Gaussian envelope."""
        self.width = self.adimensionalize_length(self.width)
        self.center = self.adimensionalize_length(self.center)
        
class GaussianConfig2D:
    """ 2D Gaussian background field configuration."""
    def __init__(
        self,
        envelope_config: dict,
        *args,
        **kwargs,
    ):
        """Initialize the Gaussian configuration.

        Args:
            envelope_config (dict): Configuration dictionary for the Gaussian envelope. keys include:
                - "I": Intensity of the Gaussian envelope.
                - "width": Width of the Gaussian envelope.
                - "center": Center position of the Gaussian envelope.
                - "exponent": Exponent for the Gaussian envelope.
        """
        self.I = envelope_config["I"]
        self.width = float_to_tuple(envelope_config["width"])
        self.center = float_to_tuple(envelope_config["center"])
        self.exponent = envelope_config["exponent"]
        super().__init__(
            *args,
            **kwargs,
        )
    
    def adimensionalize_envelope(self,):
        """ Adimensionalize the parameters of the Gaussian envelope."""
        self.width = (self.adimensionalize_length(self.width[0]), self.adimensionalize_length(self.width[1]))
        self.center = (self.adimensionalize_length(self.center[0]), self.adimensionalize_length(self.center[1]))