class Detection:
    def add_detection_noise(self,):
        for beam, beam_values in self.beams.items():
            beam_values.add_noise(
                noise = self.solver.detection_noise,
            )