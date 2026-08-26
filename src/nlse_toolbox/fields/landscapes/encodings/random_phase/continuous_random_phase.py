import numpy as np


class ContinuousRandomSpecklePhaseMask:
    def gen_random_phase_mask(
        self,
        box,
        speckle_size,
        seed=None,
    ):
        ny, nx = box.mesh.field_shape
        dy, dx = box.mesh.dy, box.mesh.dx
        
        rng = np.random.default_rng(seed)

        # Random complex spectrum
        noise = (
            rng.standard_normal((ny, nx))
            + 1j * rng.standard_normal((ny, nx))
        )

        # Spatial frequencies
        fx = np.fft.fftfreq(nx, d=dx)
        fy = np.fft.fftfreq(ny, d=dy)

        FX, FY = np.meshgrid(fx, fy)

        k2 = FX**2 + FY**2

        # Gaussian low-pass filter
        sigma_f = 1.0 / speckle_size

        filter_ = np.exp(
            -k2 / (2 * sigma_f**2)
        )

        # Filter random spatial frequencies
        field = np.fft.ifft2(
            noise * filter_
        ).real

        # Normalize to [0, 1]
        field -= field.min()
        field /= field.max()

        # Convert to phase [0, 2*pi]
        phase = 2 * np.pi * field

        self.random_phase_mask = phase
            
    def add_random_phase(self,):
        self.field *= np.exp(1.j * self.random_phase_mask)